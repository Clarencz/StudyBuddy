from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import openai
import json
import os
from src.models.user import User, db
from src.models.ai_tutor import AIConversation, AIMessage, Flashcard, PracticeTest
from src.models.document import Document
from src.routes.auth import token_required, sanitize_input

ai_bp = Blueprint('ai', __name__)

# Initialize OpenAI client
openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_ai_response(messages, conversation_type='qa'):
    """Get response from OpenAI API"""
    try:
        system_prompts = {
            'qa': "You are StudyBuddy AI, a helpful and knowledgeable tutor. Provide clear, accurate, and educational responses to student questions. Always encourage learning and critical thinking.",
            'summary': "You are StudyBuddy AI. Create concise, well-structured summaries that capture the key points and main ideas. Use bullet points and clear headings when appropriate.",
            'flashcard': "You are StudyBuddy AI. Generate educational flashcards with clear questions and comprehensive answers. Focus on key concepts, definitions, and important facts.",
            'practice_test': "You are StudyBuddy AI. Create practice test questions with multiple choice, true/false, and short answer formats. Include detailed explanations for correct answers."
        }
        
        system_message = system_prompts.get(conversation_type, system_prompts['qa'])
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                *messages
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"I'm sorry, I'm having trouble processing your request right now. Please try again later."

@ai_bp.route('/conversations', methods=['GET'])
@token_required
def get_conversations(current_user):
    """Get user's AI conversations"""
    try:
        conversations = AIConversation.query.filter_by(user_id=current_user.id).order_by(
            AIConversation.updated_at.desc()
        ).all()
        
        return jsonify({
            'conversations': [conv.to_dict() for conv in conversations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch conversations'}), 500

@ai_bp.route('/conversations', methods=['POST'])
@token_required
def create_conversation(current_user):
    """Create a new AI conversation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = sanitize_input(data)
        
        conversation_type = data.get('type', 'qa')
        if conversation_type not in ['qa', 'summary', 'flashcard', 'practice_test']:
            return jsonify({'error': 'Invalid conversation type'}), 400
        
        conversation = AIConversation(
            user_id=current_user.id,
            room_id=data.get('room_id'),
            conversation_type=conversation_type,
            title=data.get('title', f'New {conversation_type.title()} Session')
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify({
            'message': 'Conversation created',
            'conversation': conversation.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create conversation'}), 500

@ai_bp.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, conversation_id):
    """Get messages from a conversation"""
    try:
        conversation = AIConversation.query.filter_by(
            id=conversation_id,
            user_id=current_user.id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        messages = AIMessage.query.filter_by(
            conversation_id=conversation_id
        ).order_by(AIMessage.timestamp.asc()).all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch messages'}), 500

@ai_bp.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
@token_required
def send_message(current_user, conversation_id):
    """Send a message to AI tutor"""
    try:
        data = request.get_json()
        if not data or not data.get('content'):
            return jsonify({'error': 'Message content is required'}), 400
        
        data = sanitize_input(data)
        
        conversation = AIConversation.query.filter_by(
            id=conversation_id,
            user_id=current_user.id
        ).first()
        
        if not conversation:
            return jsonify({'error': 'Conversation not found'}), 404
        
        # Save user message
        user_message = AIMessage(
            conversation_id=conversation_id,
            role='user',
            content=data['content']
        )
        db.session.add(user_message)
        
        # Get conversation history for context
        previous_messages = AIMessage.query.filter_by(
            conversation_id=conversation_id
        ).order_by(AIMessage.timestamp.asc()).limit(10).all()
        
        # Prepare messages for AI
        ai_messages = []
        for msg in previous_messages:
            ai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        ai_messages.append({
            "role": "user",
            "content": data['content']
        })
        
        # Get AI response
        ai_response = get_ai_response(ai_messages, conversation.conversation_type)
        
        # Save AI response
        ai_message = AIMessage(
            conversation_id=conversation_id,
            role='assistant',
            content=ai_response
        )
        db.session.add(ai_message)
        
        # Update conversation
        conversation.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'user_message': user_message.to_dict(),
            'ai_message': ai_message.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to send message'}), 500

@ai_bp.route('/generate-summary', methods=['POST'])
@token_required
def generate_summary(current_user):
    """Generate summary from text or document"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = sanitize_input(data)
        
        text_content = data.get('text')
        document_id = data.get('document_id')
        
        if not text_content and not document_id:
            return jsonify({'error': 'Text content or document ID required'}), 400
        
        # Get text from document if document_id provided
        if document_id:
            document = Document.query.filter_by(
                id=document_id,
                uploader_id=current_user.id
            ).first()
            
            if not document:
                return jsonify({'error': 'Document not found'}), 404
            
            text_content = document.extracted_text
        
        if not text_content:
            return jsonify({'error': 'No text content available'}), 400
        
        # Generate summary using AI
        messages = [
            {"role": "user", "content": f"Please provide a comprehensive summary of the following text:\n\n{text_content}"}
        ]
        
        summary = get_ai_response(messages, 'summary')
        
        return jsonify({
            'summary': summary
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to generate summary'}), 500

@ai_bp.route('/generate-flashcards', methods=['POST'])
@token_required
def generate_flashcards(current_user):
    """Generate flashcards from text or document"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = sanitize_input(data)
        
        text_content = data.get('text')
        document_id = data.get('document_id')
        count = min(data.get('count', 10), 20)  # Limit to 20 flashcards
        
        if not text_content and not document_id:
            return jsonify({'error': 'Text content or document ID required'}), 400
        
        # Get text from document if document_id provided
        if document_id:
            document = Document.query.filter_by(
                id=document_id,
                uploader_id=current_user.id
            ).first()
            
            if not document:
                return jsonify({'error': 'Document not found'}), 404
            
            text_content = document.extracted_text
        
        if not text_content:
            return jsonify({'error': 'No text content available'}), 400
        
        # Generate flashcards using AI
        messages = [
            {"role": "user", "content": f"Create {count} educational flashcards from the following text. Format as JSON with 'question' and 'answer' fields:\n\n{text_content}"}
        ]
        
        ai_response = get_ai_response(messages, 'flashcard')
        
        # Try to parse JSON response
        try:
            flashcards_data = json.loads(ai_response)
            if not isinstance(flashcards_data, list):
                flashcards_data = [flashcards_data]
        except:
            # If JSON parsing fails, create a simple flashcard
            flashcards_data = [
                {
                    "question": "Generated Flashcard",
                    "answer": ai_response
                }
            ]
        
        # Save flashcards to database
        saved_flashcards = []
        for card_data in flashcards_data[:count]:
            flashcard = Flashcard(
                user_id=current_user.id,
                document_id=document_id,
                question=card_data.get('question', 'Generated Question'),
                answer=card_data.get('answer', 'Generated Answer'),
                difficulty=card_data.get('difficulty', 'medium'),
                category=data.get('category', 'General')
            )
            db.session.add(flashcard)
            saved_flashcards.append(flashcard)
        
        db.session.commit()
        
        return jsonify({
            'flashcards': [card.to_dict() for card in saved_flashcards]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to generate flashcards'}), 500

@ai_bp.route('/flashcards', methods=['GET'])
@token_required
def get_flashcards(current_user):
    """Get user's flashcards"""
    try:
        flashcards = Flashcard.query.filter_by(user_id=current_user.id).order_by(
            Flashcard.created_at.desc()
        ).all()
        
        return jsonify({
            'flashcards': [card.to_dict() for card in flashcards]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch flashcards'}), 500

@ai_bp.route('/flashcards/<int:flashcard_id>/review', methods=['POST'])
@token_required
def review_flashcard(current_user, flashcard_id):
    """Review a flashcard (mark as correct/incorrect)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        flashcard = Flashcard.query.filter_by(
            id=flashcard_id,
            user_id=current_user.id
        ).first()
        
        if not flashcard:
            return jsonify({'error': 'Flashcard not found'}), 404
        
        is_correct = data.get('correct', False)
        
        # Update flashcard statistics
        flashcard.times_reviewed += 1
        if is_correct:
            flashcard.correct_count += 1
        
        flashcard.last_reviewed = datetime.utcnow()
        
        # Calculate next review date based on spaced repetition
        if is_correct:
            days_to_add = min(flashcard.correct_count * 2, 30)
        else:
            days_to_add = 1
        
        flashcard.next_review = datetime.utcnow() + timedelta(days=days_to_add)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Flashcard reviewed',
            'flashcard': flashcard.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to review flashcard'}), 500

@ai_bp.route('/generate-practice-test', methods=['POST'])
@token_required
def generate_practice_test(current_user):
    """Generate a practice test from text or document"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = sanitize_input(data)
        
        text_content = data.get('text')
        document_id = data.get('document_id')
        question_count = min(data.get('question_count', 10), 20)
        
        if not text_content and not document_id:
            return jsonify({'error': 'Text content or document ID required'}), 400
        
        # Get text from document if document_id provided
        if document_id:
            document = Document.query.filter_by(
                id=document_id,
                uploader_id=current_user.id
            ).first()
            
            if not document:
                return jsonify({'error': 'Document not found'}), 404
            
            text_content = document.extracted_text
        
        if not text_content:
            return jsonify({'error': 'No text content available'}), 400
        
        # Generate practice test using AI
        messages = [
            {"role": "user", "content": f"Create a practice test with {question_count} questions from the following text. Include multiple choice, true/false, and short answer questions. Format as JSON:\n\n{text_content}"}
        ]
        
        ai_response = get_ai_response(messages, 'practice_test')
        
        # Create practice test
        practice_test = PracticeTest(
            user_id=current_user.id,
            document_id=document_id,
            title=data.get('title', 'Generated Practice Test'),
            questions=ai_response,
            total_questions=question_count
        )
        
        db.session.add(practice_test)
        db.session.commit()
        
        return jsonify({
            'practice_test': practice_test.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to generate practice test'}), 500

@ai_bp.route('/practice-tests', methods=['GET'])
@token_required
def get_practice_tests(current_user):
    """Get user's practice tests"""
    try:
        tests = PracticeTest.query.filter_by(user_id=current_user.id).order_by(
            PracticeTest.created_at.desc()
        ).all()
        
        return jsonify({
            'practice_tests': [test.to_dict() for test in tests]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch practice tests'}), 500

