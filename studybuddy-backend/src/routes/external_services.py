from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import requests
import json
import os
import uuid
from src.models.user import User, db
from src.models.study_room import StudyRoom
from src.routes.auth import token_required, sanitize_input

external_bp = Blueprint('external', __name__)

# Google Meet configuration (would need actual OAuth setup in production)
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your_google_client_id')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your_google_client_secret')

# Zoom configuration (would need actual OAuth setup in production)
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID', 'your_zoom_client_id')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET', 'your_zoom_client_secret')

@external_bp.route('/meeting/create', methods=['POST'])
@token_required
def create_meeting(current_user):
    """Create a video meeting for a study room"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = sanitize_input(data)
        
        room_id = data.get('room_id')
        platform = data.get('platform', 'google_meet')  # google_meet or zoom
        
        if not room_id:
            return jsonify({'error': 'Room ID is required'}), 400
        
        # Verify user has access to the room
        room = StudyRoom.query.get(room_id)
        if not room:
            return jsonify({'error': 'Room not found'}), 404
        
        # Check if user is owner or member
        if room.owner_id != current_user.id:
            from src.models.study_room import RoomMembership
            membership = RoomMembership.query.filter_by(
                user_id=current_user.id,
                room_id=room_id,
                is_active=True
            ).first()
            if not membership:
                return jsonify({'error': 'Access denied'}), 403
        
        # Generate meeting based on platform
        if platform == 'google_meet':
            meeting_data = create_google_meet(room, current_user)
        elif platform == 'zoom':
            meeting_data = create_zoom_meeting(room, current_user)
        else:
            return jsonify({'error': 'Unsupported platform'}), 400
        
        if not meeting_data:
            return jsonify({'error': 'Failed to create meeting'}), 500
        
        # Update room with meeting URL
        room.meeting_url = meeting_data['join_url']
        db.session.commit()
        
        return jsonify({
            'meeting_id': meeting_data['id'],
            'join_url': meeting_data['join_url'],
            'password': meeting_data.get('password'),
            'platform': platform
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create meeting'}), 500

def create_google_meet(room, user):
    """Create Google Meet meeting (simplified implementation)"""
    # In production, this would use Google Calendar API to create an event with Meet
    # For demo purposes, we'll generate a mock meeting
    
    meeting_id = str(uuid.uuid4())[:8]
    
    return {
        'id': meeting_id,
        'join_url': f"https://meet.google.com/{meeting_id}",
        'platform': 'google_meet'
    }

def create_zoom_meeting(room, user):
    """Create Zoom meeting (simplified implementation)"""
    # In production, this would use Zoom API to create a meeting
    # For demo purposes, we'll generate a mock meeting
    
    meeting_id = str(uuid.uuid4().int)[:10]
    password = str(uuid.uuid4())[:6]
    
    # Mock Zoom API call structure (would be real API call in production)
    meeting_data = {
        'topic': f"StudyBuddy - {room.name}",
        'type': 2,  # Scheduled meeting
        'start_time': datetime.utcnow().isoformat() + 'Z',
        'duration': 120,  # 2 hours
        'timezone': 'UTC',
        'password': password,
        'settings': {
            'host_video': True,
            'participant_video': True,
            'join_before_host': True,
            'mute_upon_entry': False,
            'watermark': False,
            'use_pmi': False,
            'approval_type': 0,
            'audio': 'both',
            'auto_recording': 'none'
        }
    }
    
    return {
        'id': meeting_id,
        'join_url': f"https://zoom.us/j/{meeting_id}?pwd={password}",
        'password': password,
        'platform': 'zoom'
    }

@external_bp.route('/meeting/<int:room_id>', methods=['GET'])
@token_required
def get_meeting_info(current_user, room_id):
    """Get meeting information for a room"""
    try:
        room = StudyRoom.query.get(room_id)
        if not room:
            return jsonify({'error': 'Room not found'}), 404
        
        # Check access
        if room.owner_id != current_user.id:
            from src.models.study_room import RoomMembership
            membership = RoomMembership.query.filter_by(
                user_id=current_user.id,
                room_id=room_id,
                is_active=True
            ).first()
            if not membership:
                return jsonify({'error': 'Access denied'}), 403
        
        if not room.meeting_url:
            return jsonify({'error': 'No meeting scheduled for this room'}), 404
        
        return jsonify({
            'meeting_url': room.meeting_url,
            'room_name': room.name
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get meeting info'}), 500

@external_bp.route('/integrations/status', methods=['GET'])
@token_required
def get_integration_status(current_user):
    """Get status of external integrations"""
    try:
        # In production, this would check actual OAuth tokens and permissions
        integrations = {
            'google_meet': {
                'connected': False,  # Would check OAuth token
                'name': 'Google Meet',
                'description': 'Create and join Google Meet calls directly from study rooms'
            },
            'zoom': {
                'connected': False,  # Would check OAuth token
                'name': 'Zoom',
                'description': 'Create and join Zoom meetings directly from study rooms'
            },
            'google_drive': {
                'connected': False,  # Would check OAuth token
                'name': 'Google Drive',
                'description': 'Import documents directly from Google Drive'
            },
            'dropbox': {
                'connected': False,  # Would check OAuth token
                'name': 'Dropbox',
                'description': 'Import documents directly from Dropbox'
            }
        }
        
        return jsonify({'integrations': integrations}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get integration status'}), 500

@external_bp.route('/integrations/connect/<platform>', methods=['POST'])
@token_required
def connect_integration(current_user, platform):
    """Connect to external service (OAuth flow would happen here)"""
    try:
        supported_platforms = ['google_meet', 'zoom', 'google_drive', 'dropbox']
        
        if platform not in supported_platforms:
            return jsonify({'error': 'Unsupported platform'}), 400
        
        # In production, this would initiate OAuth flow
        # For demo purposes, we'll simulate connection
        
        oauth_url = f"https://oauth.{platform}.com/authorize?client_id=demo&redirect_uri={request.host_url}external/callback/{platform}"
        
        return jsonify({
            'oauth_url': oauth_url,
            'message': f'Redirect user to {platform} OAuth'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to initiate connection'}), 500

@external_bp.route('/callback/<platform>', methods=['GET'])
def oauth_callback(platform):
    """Handle OAuth callback from external services"""
    try:
        code = request.args.get('code')
        state = request.args.get('state')  # Should contain user info
        
        if not code:
            return jsonify({'error': 'Authorization failed'}), 400
        
        # In production, exchange code for access token
        # Store token securely associated with user
        
        return jsonify({
            'message': f'{platform} connected successfully',
            'redirect_url': '/dashboard'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'OAuth callback failed'}), 500

@external_bp.route('/whiteboard/save', methods=['POST'])
@token_required
def save_whiteboard(current_user):
    """Save whiteboard data for a room"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        room_id = data.get('room_id')
        whiteboard_data = data.get('whiteboard_data')
        
        if not room_id or not whiteboard_data:
            return jsonify({'error': 'Room ID and whiteboard data required'}), 400
        
        room = StudyRoom.query.get(room_id)
        if not room:
            return jsonify({'error': 'Room not found'}), 404
        
        # Check access
        from src.models.study_room import RoomMembership
        membership = RoomMembership.query.filter_by(
            user_id=current_user.id,
            room_id=room_id,
            is_active=True
        ).first()
        
        if not membership:
            return jsonify({'error': 'Access denied'}), 403
        
        # Save whiteboard data
        room.whiteboard_data = json.dumps(whiteboard_data)
        db.session.commit()
        
        return jsonify({'message': 'Whiteboard saved successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save whiteboard'}), 500

@external_bp.route('/whiteboard/<int:room_id>', methods=['GET'])
@token_required
def get_whiteboard(current_user, room_id):
    """Get whiteboard data for a room"""
    try:
        room = StudyRoom.query.get(room_id)
        if not room:
            return jsonify({'error': 'Room not found'}), 404
        
        # Check access
        from src.models.study_room import RoomMembership
        membership = RoomMembership.query.filter_by(
            user_id=current_user.id,
            room_id=room_id,
            is_active=True
        ).first()
        
        if not membership:
            return jsonify({'error': 'Access denied'}), 403
        
        whiteboard_data = json.loads(room.whiteboard_data) if room.whiteboard_data else {}
        
        return jsonify({'whiteboard_data': whiteboard_data}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get whiteboard data'}), 500

