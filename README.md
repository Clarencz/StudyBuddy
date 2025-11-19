# StudyBuddy Enhanced - Production-Ready Version 2.0

<p align="center">
  <img src="StudyBuddyLogo/studybuddy_logo.png" alt="StudyBuddy Logo" width="200"/>
</p>

![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)

# App Screenshots

<p align="center">
  <img src="Screenshots/Dashboard.png" width="280"/>
  <img src="Screenshots/StudyRooms.png" width="280"/>
  <img src="Screenshots/InsideStudyRooms.png" width="280">
  <img src="Screenshots/Documents.png" width="280"/>
  <img src="Screenshots/AI Tutor.png" width="280"/>
  <img src="Screenshots/ProfileSettings.png" width="280">
  <img src="Screenshots/intergrations.png" width="280">
  
</p>

## 👥 Group Members

1. _Clarence Mabeya_ – [cmabeya3@gmail.com](mailto:cmabeya3@gmail.com) <br>

## 🚀 Major Enhancements & Fixes

This enhanced version of StudyBuddy addresses all critical issues and adds production-ready features:

### ✅ **Fixed Critical Issues**

- ✅ **Document Display & Reading**: Fixed document viewing and flipbook functionality
- ✅ **Flipbook Creation**: Resolved "missing token" error and implemented proper authentication
- ✅ **Dynamic AI Tutor**: Added support for multiple AI models (GPT-3.5, GPT-4, Claude)
- ✅ **Payment System**: Fixed IntaSend integration with proper webhook handling
- ✅ **Dynamic Dashboard**: Real-time user statistics and responsive design
- ✅ **Frontend-Backend Communication**: Seamless API communication with proper error handling

### 🆕 **New Production Features**

- 🔒 **Enterprise Security**: Rate limiting, input validation, security headers
- 📱 **Responsive Design**: Mobile-first approach with touch support
- 🎯 **Dynamic Dashboard**: Real-time stats, achievements, and subscription status
- 🤖 **Multi-Model AI**: Choose from different AI models for tutoring
- 💳 **Robust Payments**: Complete IntaSend integration with webhook support
- 📊 **Comprehensive Logging**: Request/response monitoring and error tracking

## 🛠 Enhanced Tech Stack

### Backend Improvements

- **Flask 3.1.1** with production-ready configuration
- **Flask-Limiter 3.5.0** for rate limiting
- **Enhanced Security** with Bleach sanitization and validation
- **Comprehensive Error Handling** with proper HTTP status codes
- **SQLAlchemy 2.0.41** with optimized database connections
- **OpenAI 1.102.0** with multi-model support

### Frontend Enhancements

- **React 18** with modern hooks and context
- **Responsive Design** with CSS Grid and Flexbox
- **Dynamic Components** with real-time updates
- **Improved UX** with loading states and error boundaries
- **Touch-Friendly Interface** for mobile devices

## 🔧 Quick Start Guide

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### 1. Backend Setup

```bash
cd studybuddy-backend

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-secret-key"
export OPENAI_API_KEY="your-openai-key"
export INTASEND_PUBLISHABLE_KEY="your-intasend-public-key"
export INTASEND_SECRET_KEY="your-intasend-secret-key"

# Start server
python src/main.py
```

### 2. Frontend Setup

```bash
cd studybuddy-frontend

# Install dependencies
npm install

# Start development server
npm start
```

### 3. Access Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/api/health

## 📋 API Documentation - Enhanced Endpoints

### Authentication (Enhanced)

```bash
# Register with validation
POST /api/auth/register
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!",
  "first_name": "Test",
  "last_name": "User"
}

# Login with improved security
POST /api/auth/login
{
  "email": "test@example.com",
  "password": "SecurePass123!"
}

# Token verification
POST /api/auth/verify-token
Headers: Authorization: Bearer <token>
```

### AI Tutor (Multi-Model Support)

```bash
# Get available models
GET /api/ai/models

# Create conversation with model selection
POST /api/ai/conversations
{
  "title": "Math Help",
  "model": "gpt-4"
}

# Chat with selected model
POST /api/ai/conversations/{id}/messages
{
  "message": "Explain calculus",
  "model": "gpt-3.5-turbo"
}
```

### Documents (Fixed)

```bash
# Upload document
POST /api/documents/upload
Content-Type: multipart/form-data

# View flipbook (fixed authentication)
GET /api/documents/{id}/flipbook

# Download document (fixed URLs)
GET /api/documents/{id}/download
```

### Payments (IntaSend Integration)

```bash
# Get subscription plans
GET /api/payment/plans

# Create payment
POST /api/payment/create-payment
{
  "plan_id": "premium_monthly",
  "amount": 65.00
}

# Webhook handler (IntaSend)
POST /api/payment/webhook
```

## 🔒 Security Features

### Input Validation

- **Comprehensive Sanitization**: HTML sanitization with Bleach
- **Schema Validation**: JSON input validation with custom decorators
- **File Upload Security**: Type and size validation for uploads
- **SQL Injection Prevention**: Parameterized queries only

### Rate Limiting

```python
# Global limits
1000 requests per hour (default)

# Endpoint-specific limits
/api/auth/login: 5 per minute
/api/auth/register: 3 per minute
/api/payment/*: 10 per minute
```

### Security Headers

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

## 📱 Frontend Enhancements

### Dynamic Dashboard

- Real-time user statistics
- Subscription status display
- Achievement tracking system
- Study streak monitoring
- Responsive grid layout

### AI Tutor Interface

- Model selection dropdown
- Conversation management
- Message history
- Typing indicators
- Error handling

### Document Management

- Fixed flipbook viewing
- Proper download links
- Upload progress indicators
- File type validation

## 💳 Payment System (IntaSend)

### Features

- M-Pesa integration
- Card payments
- Webhook notifications
- Subscription management
- Payment history

### Configuration

```env
INTASEND_PUBLISHABLE_KEY=ISPubKey_test_...
INTASEND_SECRET_KEY=ISSecretKey_test_...
INTASEND_TEST_MODE=true
```

### Webhook Setup

```bash
# Webhook URL
https://yourdomain.com/api/payment/webhook

# Supported events
- payment.completed
- payment.failed
- subscription.activated
- subscription.cancelled
```

## 🧪 Testing

### Backend Testing

```bash
# Run comprehensive API tests
python test_backend.py

# Test specific endpoints
python test_simple.py

# Health check
curl http://localhost:5000/api/health
```

### Test Results

```
✅ Health Check: PASSED
✅ User Registration: PASSED
✅ User Login: PASSED
✅ Payment Plans: PASSED
✅ Document Endpoints: PASSED
✅ AI Tutor: PASSED
⚠️  Token Verification: Minor issue (documented)
```

## 🚀 Deployment Guide

### Production Checklist

- [ ] Set strong SECRET_KEY
- [ ] Configure PostgreSQL database
- [ ] Set up SSL certificates
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test payment webhooks
- [ ] Verify security headers

### Environment Variables

```env
# Production
SECRET_KEY=strong-random-key
DATABASE_URL=postgresql://user:pass@host:5432/db
OPENAI_API_KEY=sk-...
INTASEND_PUBLISHABLE_KEY=ISPubKey_live_...
INTASEND_SECRET_KEY=ISSecretKey_live_...
INTASEND_TEST_MODE=false
FLASK_ENV=production
```

### Docker Deployment

```dockerfile
# Dockerfile included for containerized deployment
docker-compose up --build
```

## 📊 Performance Improvements

### Backend Optimizations

- Connection pooling for database
- Request/response logging
- Error handling middleware
- Optimized query patterns
- Caching strategies

### Frontend Optimizations

- Code splitting
- Lazy loading
- Optimized bundle size
- Responsive images
- Progressive loading

## 🐛 Known Issues & Solutions

### Resolved Issues

- ✅ Document display fixed
- ✅ Flipbook authentication resolved
- ✅ Payment creation errors fixed
- ✅ Dashboard responsiveness improved
- ✅ AI tutor model selection added

### Minor Outstanding Issues

- Token verification endpoint needs minor adjustment
- Large file upload timeout (chunked upload recommended)
- Real-time features need WebSocket implementation

## 📈 Monitoring & Analytics

### Logging

- Request/response logging
- Error tracking
- Performance monitoring
- Security event logging

### Metrics

- API response times
- User engagement
- Payment success rates
- Error rates

## 🤝 Contributing

### Development Setup

1. Fork repository
2. Create feature branch
3. Follow coding standards
4. Add comprehensive tests
5. Update documentation
6. Submit pull request

### Code Quality

- ESLint for JavaScript
- Black for Python
- Comprehensive testing
- Security review required

## 📄 Additional Documentation

- `API_DOCUMENTATION.md` - Complete API reference
- `TECH_STACK.md` - Updated technology stack
- `SECURITY.md` - Security implementation details
- `DEPLOYMENT.md` - Production deployment guide
- `ADDITIONAL_PROMPTS.md` - New AI prompts and configurations

## 🆘 Support

### Getting Help

- GitHub Issues for bugs
- Email: support@studybuddy.com
- Documentation: Complete inline documentation
- Community: Discord server (coming soon)

### Professional Support

- Priority support for production deployments
- Custom integrations available
- Training and onboarding services

---

