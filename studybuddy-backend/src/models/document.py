from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from src.extensions import db 

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'))  # Optional, if shared in a room
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    mime_type = db.Column(db.String(100))
    document_type = db.Column(db.String(20), default='pdf')  # pdf, doc, txt, etc.
    is_processed = db.Column(db.Boolean, default=False)
    processing_status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    extracted_text = db.Column(db.Text)
    page_count = db.Column(db.Integer)
    flipbook_url = db.Column(db.String(500))  # URL to flipbook version
    thumbnail_url = db.Column(db.String(500))
    is_public = db.Column(db.Boolean, default=False)
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flashcards = db.relationship('Flashcard', backref='document', lazy=True)
    practice_tests = db.relationship('PracticeTest', backref='document', lazy=True)

    def get_file_size_formatted(self):
        if not self.file_size:
            return "Unknown"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def get_file_extension(self):
        return os.path.splitext(self.original_filename)[1].lower()

    def is_pdf(self):
        return self.get_file_extension() == '.pdf'

    def is_image(self):
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return self.get_file_extension() in image_extensions

    def can_generate_flipbook(self):
        return self.is_pdf() and self.is_processed

    def to_dict(self):
        return {
            'id': self.id,
            'uploader_id': self.uploader_id,
            'room_id': self.room_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_size_formatted': self.get_file_size_formatted(),
            'mime_type': self.mime_type,
            'document_type': self.document_type,
            'is_processed': self.is_processed,
            'processing_status': self.processing_status,
            'page_count': self.page_count,
            'flipbook_url': self.flipbook_url,
            'thumbnail_url': self.thumbnail_url,
            'is_public': self.is_public,
            'download_count': self.download_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'can_generate_flipbook': self.can_generate_flipbook()
        }

class DocumentShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    shared_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Optional, if shared with specific user
    room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'))  # Optional, if shared in room
    permissions = db.Column(db.String(20), default='read')  # read, write, admin
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'document_id': self.document_id,
            'shared_by_id': self.shared_by_id,
            'shared_with_id': self.shared_with_id,
            'room_id': self.room_id,
            'permissions': self.permissions,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

