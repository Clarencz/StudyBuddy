from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.extensions import db
# db = SQLAlchemy()

class AIConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'))  # Optional, if in a room
    conversation_type = db.Column(db.String(20), nullable=False)  # qa, summary, flashcard, practice_test
    title = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('AIMessage', backref='conversation', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_id': self.room_id,
            'conversation_type': self.conversation_type,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'message_count': len(self.messages)
        }

class AIMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('ai_conversation.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # user, assistant
    content = db.Column(db.Text, nullable=False)
    message_metadata = db.Column(db.Text)  # JSON string for additional data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'message_metadata': self.message_metadata,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(10), default='medium')  # easy, medium, hard
    category = db.Column(db.String(50))
    times_reviewed = db.Column(db.Integer, default=0)
    correct_count = db.Column(db.Integer, default=0)
    last_reviewed = db.Column(db.DateTime)
    next_review = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_id': self.document_id,
            'question': self.question,
            'answer': self.answer,
            'difficulty': self.difficulty,
            'category': self.category,
            'times_reviewed': self.times_reviewed,
            'correct_count': self.correct_count,
            'accuracy': (self.correct_count / self.times_reviewed * 100) if self.times_reviewed > 0 else 0,
            'last_reviewed': self.last_reviewed.isoformat() if self.last_reviewed else None,
            'next_review': self.next_review.isoformat() if self.next_review else None
        }

class PracticeTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    title = db.Column(db.String(100), nullable=False)
    questions = db.Column(db.Text, nullable=False)  # JSON string of questions
    user_answers = db.Column(db.Text)  # JSON string of user answers
    score = db.Column(db.Float)
    total_questions = db.Column(db.Integer)
    time_taken = db.Column(db.Integer)  # in seconds
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_id': self.document_id,
            'title': self.title,
            'score': self.score,
            'total_questions': self.total_questions,
            'time_taken': self.time_taken,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

