# StudyBuddy Enhanced - API Documentation

This document provides comprehensive documentation for the StudyBuddy Enhanced REST API. All endpoints use JSON for request and response bodies unless otherwise specified.

## 📋 Table of Contents

- [Authentication](#authentication)
- [User Management](#user-management)
- [Study Rooms](#study-rooms)
- [Payment System](#payment-system)
- [Profile Management](#profile-management)
- [Whiteboard Collaboration](#whiteboard-collaboration)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Webhooks](#webhooks)

## 🔐 Authentication

StudyBuddy Enhanced uses JWT (JSON Web Tokens) for authentication. Include the token in the `Authorization` header for protected endpoints.

### Authentication Header Format

```
Authorization: Bearer <jwt_token>
```

### Token Expiration

- Access tokens expire after 1 hour by default
- Refresh tokens can be used to obtain new access tokens
- Expired tokens will return a 401 Unauthorized response

---

## 👤 User Management

### Register User

**POST** `/api/auth/register`

Create a new user account.

**Request Body:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "username": "johndoe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!"
}
```

**Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2024-08-31T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**

- `400 Bad Request`: Invalid input data
- `409 Conflict`: Username or email already exists

---

### Login User

**POST** `/api/auth/login`

Authenticate user and receive access token.

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "subscription_status": "free"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**

- `400 Bad Request`: Missing username or password
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account is deactivated

---

### Get Current User

**GET** `/api/auth/me`

Get current authenticated user information.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "subscription_status": "premium",
    "subscription_expires": "2025-08-31T10:00:00Z",
    "created_at": "2024-08-31T10:00:00Z",
    "last_login": "2024-08-31T12:00:00Z"
  }
}
```

---

### Refresh Token

**POST** `/api/auth/refresh`

Refresh an expired access token.

**Request Body:**

```json
{
  "refresh_token": "refresh_token_here"
}
```

**Response (200 OK):**

```json
{
  "token": "new_access_token_here",
  "refresh_token": "new_refresh_token_here"
}
```

---

## 🏠 Study Rooms

### Get All Rooms

**GET** `/api/rooms`

Get all available study rooms for the authenticated user.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**

- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of rooms per page (default: 20, max: 100)
- `subject` (optional): Filter by subject
- `is_private` (optional): Filter by privacy status (true/false)

**Response (200 OK):**

```json
{
  "rooms": [
    {
      "id": 1,
      "name": "Mathematics Study Group",
      "description": "Advanced calculus and linear algebra discussions",
      "subject": "Mathematics",
      "owner_id": 1,
      "owner_name": "John Doe",
      "is_private": false,
      "is_active": true,
      "member_count": 5,
      "max_participants": 20,
      "created_at": "2024-08-31T10:00:00Z",
      "updated_at": "2024-08-31T12:00:00Z",
      "is_member": false,
      "can_join": true
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

---

### Create Study Room

**POST** `/api/rooms`

Create a new study room.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "name": "Physics Study Group",
  "description": "Weekly physics problem-solving sessions",
  "subject": "Physics",
  "max_participants": 15,
  "is_private": false,
  "room_code": "PHYS2024"
}
```

**Response (201 Created):**

```json
{
  "message": "Study room created successfully",
  "room": {
    "id": 2,
    "name": "Physics Study Group",
    "description": "Weekly physics problem-solving sessions",
    "subject": "Physics",
    "owner_id": 1,
    "is_private": false,
    "is_active": true,
    "member_count": 1,
    "max_participants": 15,
    "room_code": "PHYS2024",
    "created_at": "2024-08-31T14:00:00Z"
  }
}
```

**Error Responses:**

- `400 Bad Request`: Invalid input data
- `403 Forbidden`: Room limit reached for free users
- `409 Conflict`: Room code already exists

---

### Get Room Details

**GET** `/api/rooms/{room_id}`

Get detailed information about a specific study room.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "room": {
    "id": 1,
    "name": "Mathematics Study Group",
    "description": "Advanced calculus and linear algebra discussions",
    "subject": "Mathematics",
    "owner_id": 1,
    "owner_name": "John Doe",
    "is_private": false,
    "is_active": true,
    "member_count": 5,
    "max_participants": 20,
    "room_code": "MATH2024",
    "created_at": "2024-08-31T10:00:00Z",
    "updated_at": "2024-08-31T12:00:00Z",
    "members": [
      {
        "user_id": 1,
        "username": "johndoe",
        "role": "owner",
        "joined_at": "2024-08-31T10:00:00Z",
        "last_seen": "2024-08-31T14:30:00Z"
      }
    ],
    "whiteboard_session": {
      "id": 1,
      "is_active": true,
      "last_updated": "2024-08-31T14:25:00Z"
    }
  }
}
```

**Error Responses:**

- `404 Not Found`: Room does not exist
- `403 Forbidden`: No access to private room

---

### Join Study Room

**POST** `/api/rooms/{room_id}/join`

Join a study room.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "message": "Successfully joined the room",
  "room": {
    "id": 1,
    "name": "Mathematics Study Group",
    "member_count": 6
  },
  "membership": {
    "role": "member",
    "joined_at": "2024-08-31T14:30:00Z"
  }
}
```

**Error Responses:**

- `400 Bad Request`: Room is full or not accepting members
- `404 Not Found`: Room does not exist
- `409 Conflict`: Already a member of the room

---

### Leave Study Room

**POST** `/api/rooms/{room_id}/leave`

Leave a study room.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "message": "Successfully left the room",
  "room_active": true
}
```

**Error Responses:**

- `400 Bad Request`: Not a member of the room
- `404 Not Found`: Room does not exist

---

### Join Room by Code

**POST** `/api/rooms/join-by-code`

Join a study room using a room code.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "room_code": "MATH2024"
}
```

**Response (200 OK):**

```json
{
  "message": "Successfully joined the room",
  "room": {
    "id": 1,
    "name": "Mathematics Study Group",
    "member_count": 6
  }
}
```

---

### Get Room Members

**GET** `/api/rooms/{room_id}/members`

Get list of room members.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "members": [
    {
      "user_id": 1,
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "role": "owner",
      "joined_at": "2024-08-31T10:00:00Z",
      "last_seen": "2024-08-31T14:30:00Z",
      "is_online": true
    }
  ],
  "total_members": 5
}
```

---

## 💳 Payment System

### Get Subscription Plans

**GET** `/api/payment/plans`

Get available subscription plans.

**Response (200 OK):**

```json
{
  "plans": [
    {
      "id": "free",
      "name": "Free",
      "price": 0,
      "currency": "KES",
      "interval": "forever",
      "features": [
        "Up to 3 study rooms",
        "Basic AI tutor",
        "5 document uploads",
        "Community support",
        "Basic analytics"
      ]
    },
    {
      "id": "premium_monthly",
      "name": "Premium Monthly",
      "price": 65,
      "currency": "KES",
      "interval": "month",
      "features": [
        "Unlimited study rooms",
        "Advanced AI tutor with GPT-4",
        "Unlimited document uploads",
        "Priority support",
        "Advanced analytics",
        "Custom branding for study rooms",
        "Export study data",
        "Offline access to documents"
      ]
    },
    {
      "id": "premium_yearly",
      "name": "Premium Yearly",
      "price": 650,
      "currency": "KES",
      "interval": "year",
      "discount": "Save 83% vs monthly",
      "features": [
        "Unlimited study rooms",
        "Advanced AI tutor with GPT-4",
        "Unlimited document uploads",
        "Priority support",
        "Advanced analytics",
        "Custom branding for study rooms",
        "Export study data",
        "Offline access to documents"
      ]
    }
  ]
}
```

---

### Create Payment

**POST** `/api/payment/create-payment`

Create a payment request for subscription.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "plan_id": "premium_yearly"
}
```

**Response (201 Created):**

```json
{
  "payment_id": "pay_123456789",
  "checkout_url": "https://checkout.intasend.com/checkout/abc123",
  "amount": 650,
  "currency": "KES",
  "plan_id": "premium_yearly",
  "expires_at": "2024-08-31T15:00:00Z",
  "api_ref": "ISL_abc123def456"
}
```

**Error Responses:**

- `400 Bad Request`: Invalid plan ID
- `409 Conflict`: Active subscription already exists

---

### Payment Webhook

**POST** `/api/payment/webhook`

Webhook endpoint for IntaSend payment notifications.

**Headers:**

```
X-IntaSend-Signature: <webhook_signature>
```

**Request Body (from IntaSend):**

```json
{
  "id": "payment_123",
  "api_ref": "ISL_abc123def456",
  "state": "COMPLETE",
  "provider": "M-PESA",
  "charges": 650,
  "net_amount": 650,
  "currency": "KES",
  "value": 650,
  "account": "254712345678",
  "created_at": "2024-08-31T14:30:00Z",
  "updated_at": "2024-08-31T14:31:00Z"
}
```

**Response (200 OK):**

```json
{
  "message": "Webhook processed successfully"
}
```

---

### Get Subscription Status

**GET** `/api/payment/status`

Get current user's subscription status.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "subscription_status": "premium",
  "plan_id": "premium_yearly",
  "expires_at": "2025-08-31T14:30:00Z",
  "is_active": true,
  "auto_renew": true,
  "features": {
    "max_study_rooms": -1,
    "max_document_uploads": -1,
    "ai_tutor_level": "advanced",
    "priority_support": true,
    "advanced_analytics": true
  }
}
```

---

### Cancel Subscription

**POST** `/api/payment/cancel`

Cancel premium subscription.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "message": "Subscription cancelled successfully",
  "expires_at": "2025-08-31T14:30:00Z",
  "access_until": "2025-08-31T14:30:00Z"
}
```

---

### Get Payment History

**GET** `/api/payment/history`

Get user's payment history.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**

- `limit` (optional): Number of records (default: 10, max: 50)

**Response (200 OK):**

```json
{
  "payments": [
    {
      "id": 1,
      "plan_id": "premium_yearly",
      "amount": 650,
      "currency": "KES",
      "status": "completed",
      "payment_method": "M-PESA",
      "api_ref": "ISL_abc123def456",
      "created_at": "2024-08-31T14:30:00Z",
      "completed_at": "2024-08-31T14:31:00Z"
    }
  ]
}
```

---

## 👤 Profile Management

### Get Profile Settings

**GET** `/api/profile/settings`

Get user's profile settings.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "profile": {
    "bio": "Computer Science student passionate about AI and machine learning",
    "learning_goals": [
      "Master calculus",
      "Learn Python programming",
      "Understand machine learning"
    ],
    "preferred_subjects": ["Mathematics", "Computer Science", "Physics"],
    "is_public": true,
    "show_email": false,
    "show_study_stats": true,
    "timezone": "Africa/Nairobi",
    "language_preference": "en",
    "notification_preferences": {
      "email_notifications": true,
      "study_reminders": true,
      "room_invitations": true,
      "achievement_alerts": true
    }
  }
}
```

---

### Update Profile Settings

**PUT** `/api/profile/settings`

Update user's profile settings.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "bio": "Updated bio text",
  "learning_goals": ["New learning goal"],
  "preferred_subjects": ["Mathematics", "Physics"],
  "is_public": false,
  "show_email": false,
  "show_study_stats": true,
  "timezone": "Africa/Nairobi",
  "language_preference": "en",
  "notification_preferences": {
    "email_notifications": false,
    "study_reminders": true,
    "room_invitations": true,
    "achievement_alerts": false
  }
}
```

**Response (200 OK):**

```json
{
  "message": "Profile settings updated successfully",
  "profile": {
    "bio": "Updated bio text",
    "learning_goals": ["New learning goal"],
    "preferred_subjects": ["Mathematics", "Physics"],
    "is_public": false,
    "show_email": false,
    "show_study_stats": true,
    "timezone": "Africa/Nairobi",
    "language_preference": "en",
    "notification_preferences": {
      "email_notifications": false,
      "study_reminders": true,
      "room_invitations": true,
      "achievement_alerts": false
    }
  }
}
```

---

### Get LMS Integrations

**GET** `/api/profile/lms/integrations`

Get user's LMS integrations.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "integrations": [
    {
      "id": 1,
      "lms_type": "canvas",
      "lms_name": "Canvas LMS",
      "server_url": "https://university.instructure.com",
      "username": "johndoe",
      "is_active": true,
      "last_sync": "2024-08-31T12:00:00Z",
      "created_at": "2024-08-30T10:00:00Z"
    }
  ]
}
```

---

### Connect LMS

**POST** `/api/profile/lms/connect`

Connect to a Learning Management System.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "lms_type": "canvas",
  "server_url": "https://university.instructure.com",
  "username": "johndoe",
  "password": "secure_password",
  "api_token": "optional_api_token"
}
```

**Response (201 Created):**

```json
{
  "message": "LMS integration created successfully",
  "integration": {
    "id": 2,
    "lms_type": "canvas",
    "lms_name": "Canvas LMS",
    "server_url": "https://university.instructure.com",
    "username": "johndoe",
    "is_active": true,
    "created_at": "2024-08-31T14:30:00Z"
  }
}
```

---

### Get Activity History

**GET** `/api/profile/activity`

Get user's activity history.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**

- `limit` (optional): Number of activities (default: 10, max: 100)
- `activity_type` (optional): Filter by activity type

**Response (200 OK):**

```json
{
  "activities": [
    {
      "id": 1,
      "activity_type": "room_joined",
      "description": "Joined Mathematics Study Group",
      "room_id": 1,
      "room_name": "Mathematics Study Group",
      "timestamp": "2024-08-31T14:30:00Z"
    },
    {
      "id": 2,
      "activity_type": "payment_completed",
      "description": "Upgraded to Premium Yearly subscription",
      "amount": 650,
      "currency": "KES",
      "timestamp": "2024-08-31T14:31:00Z"
    }
  ]
}
```

---

## 🎨 Whiteboard Collaboration

### Get Whiteboard Session

**GET** `/api/rooms/{room_id}/whiteboard`

Get whiteboard session for a study room.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
{
  "whiteboard": {
    "id": 1,
    "room_id": 1,
    "is_active": true,
    "canvas_data": {
      "objects": [],
      "background": "#ffffff"
    },
    "created_at": "2024-08-31T10:00:00Z",
    "updated_at": "2024-08-31T14:30:00Z"
  },
  "collaboration_events": [
    {
      "id": 1,
      "user_id": 1,
      "username": "johndoe",
      "event_type": "draw",
      "timestamp": "2024-08-31T14:25:00Z"
    }
  ]
}
```

---

### Update Whiteboard

**POST** `/api/rooms/{room_id}/whiteboard`

Update whiteboard canvas data.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "canvas_data": {
    "objects": [
      {
        "type": "path",
        "path": "M 10 10 L 50 50",
        "stroke": "#000000",
        "strokeWidth": 2
      }
    ],
    "background": "#ffffff"
  },
  "event_type": "draw"
}
```

**Response (200 OK):**

```json
{
  "message": "Whiteboard updated successfully",
  "whiteboard": {
    "id": 1,
    "room_id": 1,
    "updated_at": "2024-08-31T14:35:00Z"
  }
}
```

---

## ❌ Error Handling

### Error Response Format

All error responses follow a consistent format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "Additional error details"
  },
  "timestamp": "2024-08-31T14:30:00Z"
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate)
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

### Common Error Codes

- `INVALID_TOKEN`: JWT token is invalid or expired
- `MISSING_FIELD`: Required field is missing
- `INVALID_FORMAT`: Field format is invalid
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `ACCESS_DENIED`: User doesn't have permission
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `PAYMENT_FAILED`: Payment processing failed
- `SUBSCRIPTION_REQUIRED`: Premium subscription required

---

## 🚦 Rate Limiting

### Rate Limits

- **Authentication endpoints**: 5 requests per minute per IP
- **General API endpoints**: 100 requests per minute per user
- **Payment endpoints**: 10 requests per minute per user
- **Whiteboard updates**: 60 requests per minute per user

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1630000000
```

### Rate Limit Exceeded Response

```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60,
  "timestamp": "2025-08-31T14:30:00Z"
}
```

---

## 🔗 Webhooks

### IntaSend Payment Webhook

**Endpoint**: `/api/payment/webhook`
**Method**: POST
**Content-Type**: application/json

**Signature Verification**:
The webhook includes an `X-IntaSend-Signature` header that should be verified using your webhook secret.

**Event Types**:

- `COMPLETE`: Payment completed successfully
- `FAILED`: Payment failed
- `PENDING`: Payment is pending
- `CANCELLED`: Payment was cancelled

**Webhook Payload**:

```json
{
  "id": "payment_123",
  "api_ref": "ISL_abc123def456",
  "state": "COMPLETE",
  "provider": "M-PESA",
  "charges": 650,
  "net_amount": 650,
  "currency": "KES",
  "value": 650,
  "account": "254712345678",
  "created_at": "2024-08-31T14:30:00Z",
  "updated_at": "2024-08-31T14:31:00Z"
}
```

---

## 🧪 Testing

### API Testing with cURL

**Authentication**:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "password123"}'
```

**Get Study Rooms**:

```bash
curl -X GET http://localhost:5000/api/rooms \
  -H "Authorization: Bearer your_jwt_token_here"
```

**Create Payment**:

```bash
curl -X POST http://localhost:5000/api/payment/create-payment \
  -H "Authorization: Bearer your_jwt_token_here" \
  -H "Content-Type: application/json" \
  -d '{"plan_id": "premium_yearly"}'
```

### Postman Collection

A Postman collection is available with pre-configured requests for all endpoints. Import the collection and set up environment variables for easy testing.

---

## 📞 Support

### API Support

For API-related questions and support:

- **Documentation**: This comprehensive API documentation
- **GitHub Issues**: Report bugs and request features
- **Email**: api-support@studybuddy.com
- **Response Time**: 24-48 hours for technical inquiries

### Integration Support

For help with integrating StudyBuddy Enhanced API:

- **Integration Guide**: Available in the main documentation
- **Code Examples**: Check the GitHub repository for examples
- **Professional Support**: Available for enterprise customers

---

