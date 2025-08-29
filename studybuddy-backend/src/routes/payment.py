from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import requests
import json
import os
from src.models.user import User, db
from src.routes.auth import token_required, sanitize_input

payment_bp = Blueprint('payment', __name__)

# IntaSend configuration
INTASEND_BASE_URL = "https://sandbox.intasend.com/api/v1"  # Use production URL in production
INTASEND_PUBLISHABLE_KEY = os.environ.get('INTASEND_PUBLISHABLE_KEY', 'ISPubKey_test_your_key_here')
INTASEND_SECRET_KEY = os.environ.get('INTASEND_SECRET_KEY', 'ISSecretKey_test_your_key_here')

PREMIUM_PRICE_KES = 650  # KES 650 per year as specified

def intasend_api_call(endpoint, method='GET', data=None):
    """Make API call to IntaSend"""
    url = f"{INTASEND_BASE_URL}{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'X-IntaSend-Public-API-Key': INTASEND_PUBLISHABLE_KEY,
        'Authorization': f'Bearer {INTASEND_SECRET_KEY}'
    }
    
    try:
        if method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"IntaSend API error: {e}")
        return None

@payment_bp.route('/subscription-plans', methods=['GET'])
def get_subscription_plans():
    """Get available subscription plans"""
    plans = [
        {
            'id': 'premium_yearly',
            'name': 'Premium Yearly',
            'description': 'Full access to all StudyBuddy features for one year',
            'price': PREMIUM_PRICE_KES,
            'currency': 'KES',
            'duration': 365,  # days
            'features': [
                'Unlimited study rooms',
                'Advanced AI tutor with GPT-4',
                'Unlimited document uploads',
                'Priority support',
                'Advanced analytics',
                'Custom branding for study rooms',
                'Export study data',
                'Offline access to documents'
            ]
        }
    ]
    
    return jsonify({'plans': plans}), 200

@payment_bp.route('/create-payment', methods=['POST'])
@token_required
def create_payment(current_user):
    """Create a payment request with IntaSend"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        data = sanitize_input(data)
        
        plan_id = data.get('plan_id')
        if plan_id != 'premium_yearly':
            return jsonify({'error': 'Invalid plan selected'}), 400
        
        # Create payment request with IntaSend
        payment_data = {
            'public_key': INTASEND_PUBLISHABLE_KEY,
            'amount': PREMIUM_PRICE_KES,
            'currency': 'KES',
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'country': 'KE',
            'method': 'M-PESA',  # Default to M-Pesa for Kenya
            'redirect_url': f"{request.host_url}payment/callback",
            'api_ref': f"studybuddy_{current_user.id}_{int(datetime.utcnow().timestamp())}"
        }
        
        # In a real implementation, you would call IntaSend API here
        # For demo purposes, we'll simulate the response
        payment_response = {
            'id': f"payment_{int(datetime.utcnow().timestamp())}",
            'url': f"https://sandbox.intasend.com/checkout/{payment_data['api_ref']}",
            'api_ref': payment_data['api_ref'],
            'amount': PREMIUM_PRICE_KES,
            'currency': 'KES',
            'status': 'pending'
        }
        
        # In production, uncomment this:
        # payment_response = intasend_api_call('/checkout/', 'POST', payment_data)
        # if not payment_response:
        #     return jsonify({'error': 'Payment creation failed'}), 500
        
        return jsonify({
            'payment_id': payment_response['id'],
            'checkout_url': payment_response['url'],
            'amount': payment_response['amount'],
            'currency': payment_response['currency']
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Payment creation failed'}), 500

@payment_bp.route('/callback', methods=['POST'])
def payment_callback():
    """Handle payment callback from IntaSend"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No callback data'}), 400
        
        # Verify the callback signature (implement signature verification in production)
        api_ref = data.get('api_ref')
        status = data.get('status')
        amount = data.get('amount')
        
        if not api_ref:
            return jsonify({'error': 'Invalid callback data'}), 400
        
        # Extract user ID from api_ref
        try:
            user_id = int(api_ref.split('_')[1])
        except (IndexError, ValueError):
            return jsonify({'error': 'Invalid API reference'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if status == 'COMPLETE' and amount == PREMIUM_PRICE_KES:
            # Activate premium subscription
            user.is_premium = True
            user.premium_expires = datetime.utcnow() + timedelta(days=365)
            db.session.commit()
            
            return jsonify({'message': 'Payment processed successfully'}), 200
        else:
            return jsonify({'message': 'Payment not completed'}), 200
            
    except Exception as e:
        return jsonify({'error': 'Callback processing failed'}), 500

@payment_bp.route('/subscription-status', methods=['GET'])
@token_required
def get_subscription_status(current_user):
    """Get current user's subscription status"""
    try:
        is_active = current_user.is_premium and (
            not current_user.premium_expires or 
            current_user.premium_expires > datetime.utcnow()
        )
        
        return jsonify({
            'is_premium': current_user.is_premium,
            'premium_expires': current_user.premium_expires.isoformat() if current_user.premium_expires else None,
            'is_active': is_active,
            'days_remaining': (current_user.premium_expires - datetime.utcnow()).days if current_user.premium_expires and is_active else 0
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get subscription status'}), 500

@payment_bp.route('/cancel-subscription', methods=['POST'])
@token_required
def cancel_subscription(current_user):
    """Cancel premium subscription"""
    try:
        if not current_user.is_premium:
            return jsonify({'error': 'No active subscription to cancel'}), 400
        
        # In production, you would also cancel with IntaSend if it's a recurring subscription
        current_user.is_premium = False
        current_user.premium_expires = None
        db.session.commit()
        
        return jsonify({'message': 'Subscription cancelled successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel subscription'}), 500

@payment_bp.route('/payment-history', methods=['GET'])
@token_required
def get_payment_history(current_user):
    """Get user's payment history"""
    try:
        # In a real implementation, you would store payment records in the database
        # and retrieve them here. For demo purposes, we'll return mock data
        
        history = []
        if current_user.is_premium:
            history.append({
                'id': f"payment_{current_user.id}_demo",
                'amount': PREMIUM_PRICE_KES,
                'currency': 'KES',
                'status': 'completed',
                'description': 'Premium Yearly Subscription',
                'created_at': (datetime.utcnow() - timedelta(days=30)).isoformat(),
                'expires_at': current_user.premium_expires.isoformat() if current_user.premium_expires else None
            })
        
        return jsonify({'payments': history}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get payment history'}), 500

