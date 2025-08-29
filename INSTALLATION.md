# StudyBuddy Installation Guide

## Quick Start

### Prerequisites
- Node.js 20.18.0+
- Python 3.11+
- pnpm package manager

### Backend Setup
```bash
cd studybuddy-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### Frontend Setup
```bash
cd studybuddy-frontend
pnpm install
pnpm run dev
```

### Environment Variables
Create `.env` in backend directory:
```
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
INTASEND_PUBLISHABLE_KEY=your-intasend-public-key
INTASEND_SECRET_KEY=your-intasend-secret-key
```

### Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Full Documentation
See README.md for complete setup and deployment instructions.

