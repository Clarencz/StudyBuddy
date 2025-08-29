from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os
from src.extensions import db
# db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    avatar_url = db.Column(db.String(255))
    is_premium = db.Column(db.Boolean, default=False)
    premium_expires = db.Column(db.DateTime)
    streak_count = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    total_study_time = db.Column(db.Integer, default=0)  # in minutes
    badges = db.Column(db.Text)  # JSON string of earned badges
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)
    
    # Relationships
    owned_rooms = db.relationship('StudyRoom', backref='owner', lazy=True, foreign_keys='StudyRoom.owner_id')
    room_memberships = db.relationship('RoomMembership', backref='user', lazy=True)
    ai_conversations = db.relationship('AIConversation', backref='user', lazy=True)
    uploaded_documents = db.relationship('Document', backref='uploader', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        payload = {
            'user_id': self.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, os.environ.get('SECRET_KEY', 'default-secret'), algorithm='HS256')

    def is_account_locked(self):
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def increment_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()

    def reset_failed_login(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        db.session.commit()

    def update_streak(self):
        today = datetime.utcnow().date()
        last_activity_date = self.last_activity.date() if self.last_activity else None
        
        if last_activity_date == today:
            return  # Already updated today
        elif last_activity_date == today - timedelta(days=1):
            self.streak_count += 1
        else:
            self.streak_count = 1
        
        self.last_activity = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'avatar_url': self.avatar_url,
            'is_premium': self.is_premium,
            'streak_count': self.streak_count,
            'total_study_time': self.total_study_time,
            'badges': self.badges,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


