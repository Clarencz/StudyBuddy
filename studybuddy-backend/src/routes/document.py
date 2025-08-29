from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import PyPDF2
import io
from src.models.user import User, db
from src.models.document import Document, DocumentShare
from src.routes.auth import token_required, sanitize_input

document_bp = Blueprint('document', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page_count = len(pdf_reader.pages)
            
            for page_num in range(page_count):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        
        return text.strip(), page_count
    except Exception as e:
        return "", 0

def generate_flipbook_html(document):
    """Generate HTML flipbook for PDF document"""
    try:
        flipbook_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{document.original_filename} - StudyBuddy Flipbook</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                    background: #f5f5f5;
                }}
                .flipbook-container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    overflow: hidden;
                }}
                .flipbook-header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .flipbook-content {{
                    padding: 20px;
                    line-height: 1.6;
                    white-space: pre-wrap;
                }}
                .page-info {{
                    background: #f8f9fa;
                    padding: 10px;
                    text-align: center;
                    border-top: 1px solid #dee2e6;
                }}
            </style>
        </head>
        <body>
            <div class="flipbook-container">
                <div class="flipbook-header">
                    <h1>{document.original_filename}</h1>
                    <p>StudyBuddy Interactive Document</p>
                </div>
                <div class="flipbook-content">
                    {document.extracted_text or 'Content not available'}
                </div>
                <div class="page-info">
                    <p>Pages: {document.page_count or 'Unknown'} | Uploaded: {document.created_at.strftime('%Y-%m-%d %H:%M') if document.created_at else 'Unknown'}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Save flipbook HTML
        flipbook_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'flipbooks')
        os.makedirs(flipbook_dir, exist_ok=True)
        
        flipbook_filename = f"{document.id}_flipbook.html"
        flipbook_path = os.path.join(flipbook_dir, flipbook_filename)
        
        with open(flipbook_path, 'w', encoding='utf-8') as f:
            f.write(flipbook_html)
        
        return f"/api/documents/{document.id}/flipbook"
        
    except Exception as e:
        return None

@document_bp.route('/upload', methods=['POST'])
@token_required
def upload_document(current_user):
    """Upload a document"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Save file
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Get file info
        file_size = os.path.getsize(file_path)
        mime_type = file.content_type
        
        # Create document record
        document = Document(
            uploader_id=current_user.id,
            filename=unique_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
            document_type=file_extension[1:].lower() if file_extension else 'unknown'
        )
        
        db.session.add(document)
        db.session.flush()  # Get document ID
        
        # Process document based on type
        if document.is_pdf():
            try:
                extracted_text, page_count = extract_text_from_pdf(file_path)
                document.extracted_text = extracted_text
                document.page_count = page_count
                document.is_processed = True
                document.processing_status = 'completed'
                
                # Generate flipbook
                flipbook_url = generate_flipbook_html(document)
                if flipbook_url:
                    document.flipbook_url = flipbook_url
                    
            except Exception as e:
                document.processing_status = 'failed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': document.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': 'Upload failed'}), 500

@document_bp.route('/', methods=['GET'])
@token_required
def get_documents(current_user):
    """Get user's documents"""
    try:
        documents = Document.query.filter_by(uploader_id=current_user.id).order_by(
            Document.created_at.desc()
        ).all()
        
        return jsonify({
            'documents': [doc.to_dict() for doc in documents]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch documents'}), 500

@document_bp.route('/<int:document_id>', methods=['GET'])
@token_required
def get_document(current_user, document_id):
    """Get document details"""
    try:
        document = Document.query.filter_by(
            id=document_id,
            uploader_id=current_user.id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        return jsonify({
            'document': document.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch document'}), 500

@document_bp.route('/<int:document_id>/download', methods=['GET'])
@token_required
def download_document(current_user, document_id):
    """Download a document"""
    try:
        document = Document.query.filter_by(
            id=document_id,
            uploader_id=current_user.id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        if not os.path.exists(document.file_path):
            return jsonify({'error': 'File not found on server'}), 404
        
        # Update download count
        document.download_count += 1
        db.session.commit()
        
        return send_file(
            document.file_path,
            as_attachment=True,
            download_name=document.original_filename
        )
        
    except Exception as e:
        return jsonify({'error': 'Download failed'}), 500

@document_bp.route('/<int:document_id>/flipbook', methods=['GET'])
@token_required
def view_flipbook(current_user, document_id):
    """View document flipbook"""
    try:
        document = Document.query.filter_by(
            id=document_id,
            uploader_id=current_user.id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        if not document.can_generate_flipbook():
            return jsonify({'error': 'Flipbook not available for this document'}), 400
        
        flipbook_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'flipbooks',
            f"{document.id}_flipbook.html"
        )
        
        if not os.path.exists(flipbook_path):
            # Generate flipbook if it doesn't exist
            flipbook_url = generate_flipbook_html(document)
            if not flipbook_url:
                return jsonify({'error': 'Failed to generate flipbook'}), 500
        
        return send_file(flipbook_path)
        
    except Exception as e:
        return jsonify({'error': 'Failed to view flipbook'}), 500

@document_bp.route('/<int:document_id>/share', methods=['POST'])
@token_required
def share_document(current_user, document_id):
    """Share a document with another user or room"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = sanitize_input(data)
        
        document = Document.query.filter_by(
            id=document_id,
            uploader_id=current_user.id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        share = DocumentShare(
            document_id=document_id,
            shared_by_id=current_user.id,
            shared_with_id=data.get('shared_with_id'),
            room_id=data.get('room_id'),
            permissions=data.get('permissions', 'read')
        )
        
        if data.get('expires_in_days'):
            share.expires_at = datetime.utcnow() + timedelta(days=data['expires_in_days'])
        
        db.session.add(share)
        db.session.commit()
        
        return jsonify({
            'message': 'Document shared successfully',
            'share': share.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to share document'}), 500

@document_bp.route('/<int:document_id>', methods=['DELETE'])
@token_required
def delete_document(current_user, document_id):
    """Delete a document"""
    try:
        document = Document.query.filter_by(
            id=document_id,
            uploader_id=current_user.id
        ).first()
        
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # Delete file from filesystem
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete flipbook if exists
        flipbook_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'flipbooks',
            f"{document.id}_flipbook.html"
        )
        if os.path.exists(flipbook_path):
            os.remove(flipbook_path)
        
        # Delete from database
        db.session.delete(document)
        db.session.commit()
        
        return jsonify({'message': 'Document deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete document'}), 500

@document_bp.route('/shared', methods=['GET'])
@token_required
def get_shared_documents(current_user):
    """Get documents shared with the user"""
    try:
        shares = DocumentShare.query.filter_by(shared_with_id=current_user.id).all()
        
        shared_docs = []
        for share in shares:
            if share.expires_at and share.expires_at < datetime.utcnow():
                continue  # Skip expired shares
            
            doc_data = share.document.to_dict()
            doc_data['share_info'] = share.to_dict()
            shared_docs.append(doc_data)
        
        return jsonify({
            'shared_documents': shared_docs
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch shared documents'}), 500

