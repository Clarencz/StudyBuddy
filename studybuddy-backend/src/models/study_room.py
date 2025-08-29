from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from src.extensions import db
# db = SQLAlchemy()

class StudyRoom(db.Model):
    __tablename__ = "study_room"
    
    
    id = db.Column(db.Integer, primary_key=True)
    room_code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_participants = db.Column(db.Integer, default=10)
    is_private = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    meeting_url = db.Column(db.String(255))  # Google Meet/Zoom URL
    whiteboard_data = db.Column(db.Text)  # JSON string for whiteboard state
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memberships = db.relationship('RoomMembership', backref='room', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('StudySession', backref='room', lazy=True)
    documents = db.relationship('Document', backref='room', lazy=True)

    def __init__(self, **kwargs):
        super(StudyRoom, self).__init__(**kwargs)
        if not self.room_code:
            self.room_code = self.generate_room_code()

    def generate_room_code(self):
        return str(uuid.uuid4())[:8].upper()

    def get_active_members(self):
        return [membership.user for membership in self.memberships if membership.is_active]

    def get_member_count(self):
        return len([m for m in self.memberships if m.is_active])

    def can_join(self):
        return self.is_active and self.get_member_count() < self.max_participants

    def to_dict(self):
        return {
            'id': self.id,
            'room_code': self.room_code,
            'name': self.name,
            'description': self.description,
            'subject': self.subject,
            'owner_id': self.owner_id,
            'max_participants': self.max_participants,
            'is_private': self.is_private,
            'is_active': self.is_active,
            'meeting_url': self.meeting_url,
            'member_count': self.get_member_count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RoomMembership(db.Model):
    __tablename__ = "room_membership"
    
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # owner, moderator, member
    is_active = db.Column(db.Boolean, default=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_id': self.room_id,
            'role': self.role,
            'is_active': self.is_active,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None
        }

class StudySession(db.Model):
    __tablename__ = "study_session"
    
    
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('study_room.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer, default=0)
    focus_score = db.Column(db.Integer)  # 1-100 based on activity
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_minutes': self.duration_minutes,
            'focus_score': self.focus_score,
            'notes': self.notes
        }

