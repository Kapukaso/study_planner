# Study Planner System

An AI-powered study planner that ingests subject-wise documents and automatically generates notes, cheatsheets, previous-year questions, and personalized timetables.

## 🎯 Project Status: Phase 1 MVP Complete

### ✅ What's Working

**Database Infrastructure**
- ✅ Complete SQLAlchemy ORM with 14 interconnected tables
- ✅ SQLite for local development (PostgreSQL-ready)
- ✅ Database initialization and seeding scripts
- ✅ Sample data: Operating Systems subject with topics, notes, cheatsheets, PYQs

**REST API with FastAPI**
- ✅ Subject Management (Full CRUD)
- ✅ Document Upload (PDF, DOCX, PPT, Images)
- ✅ File storage with validation (type, size limits)
- ✅ Auto-generated API docs at `/docs`
- ✅ Health monitoring endpoints

**Core Features**
- ✅ User management models
- ✅ Subject/Chapter/Topic hierarchy
- ✅ Document processing pipeline foundation
- ✅ Resource generation models (Notes, Cheatsheets, PYQs, Flashcards)
- ✅ Timetable planning models
- ✅ Progress tracking system

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd studyPlanner

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install fastapi uvicorn pydantic pydantic-settings python-multipart sqlalchemy alembic python-dotenv

# Initialize database
python scripts/init_db.py

# Seed with sample data
python scripts/seed_db.py
```

### Run the Server

```bash
uvicorn main:app --reload
```

Server runs on: **http://127.0.0.1:8000**

**API Documentation**: http://127.0.0.1:8000/docs

---

## 📚 API Endpoints

### Health Check
```
GET /health - Server health status
GET / - API information
```

### Subject Management
```
POST   /api/subjects          - Create subject
GET    /api/subjects          - List all subjects
GET    /api/subjects/{id}     - Get subject details
PUT    /api/subjects/{id}     - Update subject
DELETE /api/subjects/{id}     - Delete subject
```

### Document Upload
```
POST   /api/documents/upload  - Upload document
GET    /api/documents         - List documents
GET    /api/documents/{id}    - Get document details
DELETE /api/documents/{id}    - Delete document
```

---

## 🗄️ Database Schema

### Core Tables
- **users** - User accounts and preferences
- **subjects** - Courses/subjects being studied
- **chapters** - Chapter organization
- **topics** - Core knowledge units with difficulty scoring

### Document Processing
- **documents** - Uploaded file metadata
- **document_chunks** - Parsed text segments with classification

### Generated Resources
- **notes** - Auto-generated study notes
- **cheatsheets** - One-page summaries
- **pyqs** - Previous year questions
- **flashcards** - Active recall cards

### Planning & Progress
- **timetables** - Study schedules
- **timetable_slots** - Individual study sessions
- **user_progress** - Topic mastery tracking
- **topic_dependencies** - Prerequisite relationships

---

## 📖 Example Usage

### 1. Create a Subject

```bash
curl -X POST http://127.0.0.1:8000/api/subjects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Data Structures",
    "code": "CS201",
    "exam_date": "2026-03-20",
    "priority": 8,
    "total_marks": 100
  }'
```

### 2. Upload a Document

```bash
curl -X POST http://127.0.0.1:8000/api/documents/upload \
  -F "file=@lecture_notes.pdf" \
  -F "subject_id=<subject-id-from-step-1>"
```

### 3. List Subjects

```bash
curl http://127.0.0.1:8000/api/subjects
```

---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Validation**: Pydantic v2
- **Server**: Uvicorn
- **Document Processing**: pdfplumber, python-docx, python-pptx (ready to integrate)

---

## 📁 Project Structure

```
studyPlanner/
├── main.py                 # FastAPI application
├── src/
│   ├── config.py          # Configuration management
│   ├── api/               # API layer
│   │   ├── routers/       # Endpoint routers
│   │   ├── schemas/       # Pydantic models
│   │   ├── dependencies.py
│   │   └── exceptions.py
│   ├── database/          # Database layer
│   │   ├── base.py        # SQLAlchemy setup
│   │   └── seed.py        # Sample data
│   ├── models/            # ORM models (14 files)
│   ├── services/          # Business logic
│   │   ├── subject_service.py
│   │   └── document_service.py
│   └── utils/             # Utilities
│       └── file_storage.py
├── scripts/               # Database scripts
│   ├── init_db.py        # Initialize database
│   ├── seed_db.py        # Seed sample data
│   └── reset_db.py       # Reset database
├── .env                   # Environment config
├── requirements.txt       # Dependencies
└── study_planner.db      # SQLite database
```

---

## 🎓 Sample Data

The seed script creates:
- **User**: demo@studyplanner.com
- **Subject**: Operating Systems (60-day exam timeline)
- **Chapter**: Process Management
- **Topics**: 
  - Process Concepts (Easy, 2.0 hrs)
  - Process Synchronization (Medium, 4.0 hrs)
  - Deadlock (Hard, 5.0 hrs) ← depends on Process Synchronization
- **Resources**:
  - 1 Note with Markdown content
  - 1 Cheatsheet with formulas
  - 2 PYQs from 2023 exams
  - 2 Flashcards
- **Timetable**: 60-day plan with 2 study slots

---

## 🔮 Roadmap

### Phase 2 (In Progress)
- [ ] PDF text extraction engine
- [ ] DOCX/PPT parsing
- [ ] Content classification (concept, formula, definition, PYQ)
- [ ] Knowledge graph construction
- [ ] Auto-generate notes from documents
- [ ] Auto-generate cheatsheets
- [ ] PYQ extraction and categorization

### Phase 3 (Planned)
- [ ] AI/NLP integration (spaCy, transformers)
- [ ] Semantic search
- [ ] Adaptive timetable rescheduling
- [ ] Weak topic detection
- [ ] Spaced repetition algorithm
- [ ] Frontend (React/Next.js)
- [ ] User authentication

---

## 🧪 Testing

### Run API Tests
```bash
python test_api.py
```

### Reset Database
```bash
python scripts/reset_db.py
```

### Interactive Testing
Open http://127.0.0.1:8000/docs for Swagger UI with interactive API testing.

---

## 📄 License

MIT License - Feel free to use for your studies!

---

## 🤝 Contributing

Contributions welcome! This is an educational project to demonstrate:
- FastAPI best practices
- SQLAlchemy ORM patterns
- Document processing pipelines
- AI-powered education tools

---

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for students who want to study smarter, not harder.**
