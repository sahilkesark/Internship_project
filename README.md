# AI-Based Career Recommendation System for Defence & Civil Services

## Overview
An intelligent career recommendation platform that helps students and aspirants find their ideal career path in Defence and Civil Services through AI-powered assessments and personalized study plans.

## 🎯 Key Features

### Comprehensive Assessment System
- **Personal Profile**: Demographics, contact information, location details
- **Physical Fitness Evaluation**: Height, weight, eyesight, medical conditions
- **Educational Background**: Qualifications, stream, grades, NCC certification
- **OLQ Assessment**: 50-question randomized test covering 10 leadership categories

### AI-Powered Recommendations
- Machine learning-based career matching
- Category-wise leadership analysis
- Personalized career suggestions with match scores
- Detailed eligibility criteria and selection process information

### Exam-Specific Study Plans
Six major exams configured with complete syllabus:
- **NDA** (National Defence Academy) - 600 hours
- **CDS** (Combined Defence Services) - 400 hours
- **AFCAT** (Air Force Common Admission Test) - 350 hours
- **UPSC CSE** (Civil Services Examination) - 2000+ hours
- **SSC CGL** (Staff Selection Commission) - 500 hours
- **State PSC** (State Public Service Commissions) - 1200 hours

### Advanced Features
- Randomized OLQ questions (no two sessions alike)
- Session-based validation for test integrity
- Strength/weakness identification
- Daily study schedules with milestones
- Recommended books and resources

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.9+)
- **Database**: SQLite with SQLAlchemy ORM
- **AI/ML**: scikit-learn (Random Forest, Gradient Boosting)
- **Data Processing**: pandas, numpy

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **Forms**: React Hook Form
- **HTTP Client**: Fetch API

### DevOps
- Docker & Docker Compose support
- FastAPI Swagger UI for API documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Node.js 14 or higher
- npm 6 or higher

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm start
```

### 3. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Docker Setup (Alternative)
```bash
docker-compose up -d
```

## 📁 Project Structure

```
career-recommendation-system/
├── backend/
│   ├── app/
│   │   ├── api/                      # REST API endpoints
│   │   ├── models/                   # Database models & schemas
│   │   ├── services/                 # Business logic layer
│   │   │   ├── question_bank_service.py     # 50 OLQ questions
│   │   │   ├── exam_config_service.py       # 6 exam configurations
│   │   │   ├── olq_service.py               # OLQ scoring engine
│   │   │   ├── recommendation_service.py    # ML recommendations
│   │   │   └── study_plan_service.py        # Study plan generator
│   │   └── utils/                    # Utility functions
│   ├── data/                         # Sample data
│   ├── tests/                        # Unit tests
│   ├── requirements.txt              # Python dependencies
│   ├── career_db.db                  # SQLite database
│   └── Dockerfile                    # Backend container config
│
├── frontend/
│   ├── src/
│   │   ├── components/               # Reusable React components
│   │   ├── pages/                    # Page components
│   │   ├── services/                 # API service layer
│   │   └── App.js                    # Main application
│   ├── public/                       # Static assets
│   ├── package.json                  # Node dependencies
│   └── Dockerfile                    # Frontend container config
│
├── scripts/                          # Utility scripts
├── docker-compose.yml                # Docker orchestration
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## 🔌 API Endpoints

### Assessment APIs
- `POST /api/assessment/start` - Start new assessment
- `PUT /api/assessment/{id}/physical` - Update physical details
- `PUT /api/assessment/{id}/education` - Update education details
- `GET /api/assessment/olq-questions` - Get randomized OLQ questions
- `POST /api/assessment/olq` - Submit OLQ responses
- `GET /api/assessment/{id}` - Get assessment details

### Recommendation APIs
- `POST /api/recommendations/generate` - Generate AI recommendations
- `GET /api/recommendations/{id}` - Get recommendation details

### Study Plan APIs
- `GET /api/study-plan/exams` - List all available exams
- `GET /api/study-plan/exams/{code}` - Get specific exam details
- `POST /api/study-plan/generate` - Generate exam-specific study plan
- `GET /api/study-plan/{id}` - Get study plan details

**Full API Documentation**: http://localhost:8000/docs (when backend is running)

## 📖 User Guide

### Complete Assessment Flow

1. **Start Assessment**
   - Enter personal details (name, DOB, contact, location)
   - Provide physical details (height, weight, eyesight, medical conditions)
   - Add educational qualifications (degree, stream, percentage, NCC)

2. **Take OLQ Test**
   - Answer 10 randomly selected questions
   - Questions assess leadership, decision-making, integrity, and more
   - Secure session-based validation

3. **View Recommendations**
   - See AI-powered career matches with match scores
   - Review detailed eligibility criteria
   - Understand the complete selection process

4. **Generate Study Plan**
   - Select your target exam (NDA/CDS/AFCAT/UPSC/SSC/State PSC)
   - Choose target exam date
   - Set daily available study hours
   - Receive customized study plan with:
     - Exam-specific syllabus
     - Daily study schedule
     - Phase-wise planning
     - Important milestones
     - Recommended books

## 🧪 OLQ Assessment Details

### Question Bank
- **Total Questions**: 50 comprehensive questions
- **Per Session**: 10 randomly selected questions
- **Question Types**: Scenario-based leadership situations
- **Correct Answers**: Distributed across all options (A, B, C, D)

### Leadership Categories (10)
1. Leadership & Team Management
2. Decision Making Under Pressure
3. Integrity & Ethics
4. Adaptability & Resilience
5. Innovation & Initiative
6. Strategic Thinking
7. Communication Skills
8. Crisis Management
9. Emotional Intelligence
10. Accountability

### Scoring
- Category-wise performance analysis
- Strength/weakness identification
- Personalized recommendations based on results

## 🎓 Exam Configurations

Each exam includes:
- Complete syllabus breakdown by subject
- Exam pattern and paper structure
- Recommended study hours
- Age limits and eligibility criteria
- Selection process stages
- Recommended books and resources
- Phase-wise study templates

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
source venv/bin/activate
pytest tests/

# Frontend tests
cd frontend
npm test
```

### Environment Variables

**Backend** (`backend/.env`):
```
DATABASE_URL=sqlite:///./career_db.db
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

**Frontend** (`frontend/.env`):
```
REACT_APP_API_URL=http://localhost:8000
```

## 🚢 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in backend
- [ ] Use strong `SECRET_KEY`
- [ ] Configure CORS properly
- [ ] Set up HTTPS
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable proper logging
- [ ] Run security audit: `npm audit fix`

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📊 System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │────────▶│   FastAPI    │────────▶│   SQLite    │
│  Frontend   │  HTTP   │   Backend    │  ORM    │  Database   │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                               │
                         ┌─────▼──────┐
                         │  ML Models │
                         │  (sklearn) │
                         └────────────┘
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - feel free to use for educational or commercial purposes.

## 🙏 Acknowledgments

- UPSC, NDA, CDS, AFCAT examination patterns and syllabi
- Defence services eligibility criteria and standards
- Leadership assessment frameworks
- Open source community

## 📧 Support

For issues, questions, or suggestions:
- Check the API documentation at http://localhost:8000/docs
- Review this README thoroughly
- Examine code comments for detailed explanations

---

**Version**: 2.0  
**Status**: Production Ready ✅  
**Last Updated**: November 2025

Made with ❤️ for aspiring defence and civil service officers
