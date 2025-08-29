# StudyBuddy - AI-Powered Collaborative Learning Platform

![StudyBuddy Logo](studybuddy_logo.png)

## Overview

StudyBuddy is a comprehensive collaborative learning platform that combines the power of artificial intelligence with social learning features to create an engaging and effective educational experience. The platform enables students to create or join study rooms, collaborate with peers, access AI-powered tutoring, and manage their learning materials in an integrated environment.

## Key Features

### 🤖 AI-Powered Tutoring

- **Intelligent Q&A System:** Get instant answers and explanations from our advanced AI tutor
- **Personalized Learning:** AI adapts to individual learning styles and progress
- **Content Generation:** Automatic creation of summaries, flashcards, and practice tests
- **Multi-Subject Support:** Comprehensive coverage across various academic disciplines

### 👥 Collaborative Study Rooms

- **Real-Time Collaboration:** Create and join study rooms with peers
- **Integrated Video Calls:** Seamless Google Meet and Zoom integration
- **Interactive Whiteboard:** Digital whiteboard for visual explanations and note-taking
- **Member Management:** Invite peers and manage study group permissions

### 📚 Smart Document Processing

- **PDF Upload and Processing:** Upload documents for AI-powered analysis
- **FlipHTML5-Style Flipbooks:** Convert PDFs to interactive, engaging flipbooks
- **Content Extraction:** AI extracts key concepts and generates study materials
- **Document Sharing:** Share processed documents within study rooms

### 🎮 Gamified Learning Experience

- **Study Streaks:** Track consecutive study days and build habits
- **Achievement Badges:** Earn badges for various learning milestones
- **Progress Analytics:** Detailed insights into learning progress and patterns
- **Leaderboards:** Friendly competition with study room members

### 🔒 Enterprise-Grade Security

- **JWT Authentication:** Secure, stateless authentication system
- **Data Encryption:** End-to-end encryption for sensitive data
- **Security Compliance:** Protection against SQL injection, XSS, CSRF, and brute-force attacks
- **Privacy Protection:** Comprehensive data privacy and user consent management

### 💳 Integrated Payment System

- **IntaSend Integration:** Secure payment processing for Kenyan users
- **Flexible Pricing:** KES 650/year for premium features
- **M-Pesa Support:** Native mobile money payment integration
- **Subscription Management:** Easy upgrade, downgrade, and cancellation

## Technology Stack

### Backend

- **Framework:** Flask 3.1.1
- **Database:** SQLAlchemy with SQLite (development) / PostgreSQL (production)
- **Authentication:** JWT with PyJWT 2.10.1
- **AI Integration:** OpenAI API with GPT-3.5-turbo and GPT-4
- **Security:** Comprehensive security implementation with Bleach, Werkzeug
- **Payment Processing:** IntaSend API integration

### Frontend

- **Framework:** React 19.1.0 with TypeScript support
- **Build Tool:** Vite 6.3.5 for fast development and optimized builds
- **UI Framework:** Tailwind CSS with shadcn/ui components
- **Icons:** Lucide React for consistent iconography
- **State Management:** React Context API
- **Routing:** React Router DOM 6.x

### Development Tools

- **Package Management:** pnpm (frontend), pip (backend)
- **Code Quality:** ESLint, Prettier for consistent code formatting
- **Testing:** Jest with React Testing Library
- **Version Control:** Git with feature branch workflow

## Project Structure

```
StudyBuddy/
├── studybuddy-backend/          # Flask backend application
│   ├── src/
│   │   ├── models/              # Database models
│   │   ├── routes/              # API route handlers
│   │   ├── static/              # Static files
│   │   └── main.py              # Application entry point
│   ├── venv/                    # Python virtual environment
│   └── requirements.txt         # Python dependencies
├── studybuddy-frontend/         # React frontend application
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Page components
│   │   ├── contexts/            # React contexts
│   │   └── App.jsx              # Main application component
│   ├── public/                  # Public assets
│   └── package.json             # Node.js dependencies
├── studybuddy_logo.png          # Application logo
├── PROMPTS.md                   # AI prompt documentation
├── TECH_STACK.md                # Technology stack details
├── SECURITY.md                  # Security implementation guide
└── README.md                    # This file
```

## Installation and Setup

### Prerequisites

- **Node.js:** Version 20.18.0 or higher
- **Python:** Version 3.11 or higher
- **pnpm:** For frontend package management
- **pip:** For backend package management

### Backend Setup

1. **Navigate to the backend directory:**

   ```bash
   cd studybuddy-backend
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables:**

   ```bash
   export SECRET_KEY="your-secret-key-here"
   export OPENAI_API_KEY="your-openai-api-key"
   export INTASEND_PUBLISHABLE_KEY="your-intasend-public-key"
   export INTASEND_SECRET_KEY="your-intasend-secret-key"
   ```

5. **Initialize database:**

   ```bash
   python src/main.py
   ```

6. **Start the backend server:**
   ```bash
   python src/main.py
   ```

The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd studybuddy-frontend
   ```

2. **Install dependencies:**

   ```bash
   pnpm install
   ```

3. **Start the development server:**
   ```bash
   pnpm run dev
   ```

The frontend will be available at `http://localhost:5173` (or the next available port)

### Environment Configuration

Create a `.env` file in the backend directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1
INTASEND_PUBLISHABLE_KEY=your-intasend-public-key
INTASEND_SECRET_KEY=your-intasend-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
ZOOM_CLIENT_ID=your-zoom-client-id
ZOOM_CLIENT_SECRET=your-zoom-client-secret
```

## API Documentation

### Authentication Endpoints

#### POST /api/auth/register

Register a new user account.

**Request Body:**

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "message": "User registered successfully",
  "token": "jwt-token-here"
}
```

#### POST /api/auth/login

Authenticate user and receive access token.

**Request Body:**

```json
{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}
```

**Response:**

```json
{
  "message": "Login successful",
  "token": "jwt-token-here",
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }
}
```

### Study Room Endpoints

#### GET /api/rooms

Get all study rooms for the authenticated user.

**Headers:**

```
Authorization: Bearer jwt-token-here
```

**Response:**

```json
{
  "rooms": [
    {
      "id": 1,
      "name": "Mathematics Study Group",
      "description": "Advanced calculus study sessions",
      "owner_id": 1,
      "created_at": "2024-08-28T10:00:00Z"
    }
  ]
}
```

#### POST /api/rooms

Create a new study room.

**Headers:**

```
Authorization: Bearer jwt-token-here
```

**Request Body:**

```json
{
  "name": "Physics Study Group",
  "description": "Weekly physics problem-solving sessions",
  "subject": "Physics",
  "max_members": 10
}
```

### AI Tutor Endpoints

#### POST /api/ai/chat

Send a message to the AI tutor.

**Headers:**

```
Authorization: Bearer jwt-token-here
```

**Request Body:**

```json
{
  "message": "Explain the concept of derivatives in calculus",
  "conversation_id": 1
}
```

**Response:**

```json
{
  "response": "A derivative represents the rate of change...",
  "conversation_id": 1,
  "message_id": 123
}
```

#### POST /api/ai/generate-flashcards

Generate flashcards from text content.

**Headers:**

```
Authorization: Bearer jwt-token-here
```

**Request Body:**

```json
{
  "content": "Text content to generate flashcards from...",
  "count": 10
}
```

## Security Features

StudyBuddy implements comprehensive security measures to protect user data and prevent common web application vulnerabilities:

### Authentication Security

- **JWT Tokens:** Stateless authentication with configurable expiration
- **Password Hashing:** Secure password storage using PBKDF2 with salt
- **Account Lockout:** Protection against brute-force attacks
- **Session Management:** Secure session handling with proper cleanup

### Input Validation

- **Server-Side Validation:** All inputs validated on the server
- **HTML Sanitization:** Prevention of XSS attacks using Bleach
- **SQL Injection Prevention:** Parameterized queries through SQLAlchemy ORM
- **CSRF Protection:** Token-based CSRF prevention

### Data Protection

- **Encryption in Transit:** TLS/HTTPS for all communications
- **Encryption at Rest:** Sensitive data encrypted in database
- **Data Minimization:** Only necessary data collected and stored
- **Privacy Controls:** User consent and data management features

## Payment Integration

StudyBuddy integrates with IntaSend for secure payment processing in Kenya:

### Supported Payment Methods

- **M-Pesa:** Mobile money payments
- **Bank Transfers:** Direct bank account transfers
- **Card Payments:** Visa and Mastercard support

### Pricing

- **Free Tier:** Basic features with limited AI interactions
- **Premium:** KES 650/year for unlimited access to all features

### Security

- **PCI DSS Compliance:** Secure payment data handling
- **Tokenization:** No sensitive payment data stored
- **Webhook Verification:** Cryptographic verification of payment notifications

## Deployment

### Development Deployment

For development and testing purposes, both frontend and backend can be run locally using the setup instructions above.

### Production Deployment

For production deployment, consider the following recommendations:

#### Backend Deployment

- **WSGI Server:** Use Gunicorn or uWSGI for production
- **Reverse Proxy:** Nginx for static file serving and SSL termination
- **Database:** PostgreSQL or MySQL for production workloads
- **Environment Variables:** Secure management of sensitive configuration

#### Frontend Deployment

- **Build Optimization:** Use `pnpm run build` for production builds
- **CDN:** Serve static assets through a Content Delivery Network
- **Caching:** Implement appropriate caching strategies
- **Monitoring:** Set up monitoring and error tracking

#### Infrastructure

- **SSL/TLS:** Implement HTTPS with valid certificates
- **Firewall:** Configure appropriate firewall rules
- **Backup:** Regular database and file backups
- **Monitoring:** Application and infrastructure monitoring

## Contributing

We welcome contributions to StudyBuddy! Please follow these guidelines:

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with appropriate tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Code Standards

- Follow existing code style and conventions
- Write comprehensive tests for new features
- Update documentation for any API changes
- Ensure all security best practices are followed

### Testing

- Run the test suite before submitting changes
- Add tests for new functionality
- Ensure all existing tests continue to pass
- Test security features thoroughly

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For support, questions, or feedback:

- **Email:** support@studybuddy.com
- **Documentation:** Refer to the comprehensive documentation files
- **Issues:** Use the GitHub issue tracker for bug reports and feature requests

## Acknowledgments

- **OpenAI:** For providing the AI capabilities that power our tutoring features
- **IntaSend:** For secure payment processing in Kenya
- **Open Source Community:** For the excellent libraries and frameworks used in this project

## Roadmap

### Upcoming Features

- **Mobile Applications:** Native iOS and Android apps
- **Advanced Analytics:** Detailed learning analytics and insights
- **Collaborative Editing:** Real-time document collaboration
- **Integration Expansion:** Additional third-party service integrations
- **Multi-language Support:** Internationalization and localization

### Long-term Vision

StudyBuddy aims to become the leading collaborative learning platform in Africa, expanding to serve students across the continent with localized features, payment methods, and educational content.

---

**StudyBuddy - Empowering Education Through AI and Collaboration**
