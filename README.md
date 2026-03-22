# Study Planner System

An AI-powered study planner that ingests subject-wise documents and automatically generates notes, cheatsheets, previous-year questions, and personalized timetables.

## 🎯 Project Status: Phase 2 Complete

### ✅ What's Working

**Frontend (New!)**
- ✅ **React + Vite + TypeScript** modern architecture.
- ✅ **Glassmorphism UI** with Tailwind CSS (Indigo/Violet dark theme).
- ✅ **Interactive Dashboard** with subject statistics.
- ✅ **Resource Viewer**: Tabbed interface for Documents, Notes, Flashcards, and PYQs.
- ✅ **Active Recall**: Interactive 3D flip-cards for flashcard study.
- ✅ **Topic-based Navigation**: Sidebar for navigating auto-generated knowledge topics.

**Database Infrastructure**
- ✅ Complete SQLAlchemy ORM with 14 interconnected tables.
- ✅ SQLite for local development (PostgreSQL-ready).
- ✅ Database initialization and seeding scripts.
- ✅ Sample data: Operating Systems subject with topics, notes, cheatsheets, PYQs.

**REST API with FastAPI**
- ✅ **Authentication**: Secure JWT-based auth with SHA256 hashing.
- ✅ **Subject & Topic Management**: Full hierarchy navigation.
- ✅ **Document Processing**: Pipeline for PDF/DOCX/PPT parsing and content classification.
- ✅ **Resource API**: Endpoints for fetching auto-generated Notes, Flashcards, and PYQs.
- ✅ **Auto-generated API docs** at `/docs`.

**Core Features**
- ✅ PDF/DOCX text extraction engine.
- ✅ Content classification (concepts, formulas, definitions, PYQs).
- ✅ Knowledge structure extraction (auto-creating chapters and topics).
- ✅ Resource generation models (Notes, Cheatsheets, PYQs, Flashcards).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### Backend Installation

```bash
# Clone the repository
git clone <repo-url>
cd studyPlanner

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Seed with sample data
python scripts/seed_db.py
```

### Frontend Installation

```bash
cd frontend
npm install
npm run build  # For production
```

### Run the System

1. **Production Mode**:
   ```bash
   # Run from root directory
   uvicorn main:app --reload
   ```
   Access at: **http://127.0.0.1:8000** (FastAPI serves the React build)

2. **Development Mode**:
   - Backend: `uvicorn main:app --reload` (Port 8000)
   - Frontend: `cd frontend && npm run dev` (Port 5173 - proxies API to 8000)

---

## 📚 API Endpoints

### Authentication
```
POST /api/auth/register - Register new user
POST /api/auth/login    - Get access token
GET  /api/auth/users/me - Get current user profile
```

### Subject & Topic Management
```
GET    /api/subjects              - List all subjects
GET    /api/subjects/{id}/topics  - List topics for a subject
GET    /api/topics/{id}/resources - Get all generated materials for a topic
```

### Document Upload & Processing
```
POST   /api/documents/upload      - Upload PDF/DOCX/PPT
POST   /api/documents/{id}/process - Trigger AI analysis
GET    /api/documents/{id}/chunks  - View classified text segments
```

---

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React.
- **Backend**: FastAPI (Python 3.12).
- **ORM**: SQLAlchemy 2.0.
- **Database**: SQLite (dev) / PostgreSQL (prod).
- **Security**: JWT, Passlib (SHA256_Crypt).
- **Document Processing**: pdfplumber, python-docx, python-pptx, pytesseract.

---

## 📁 Project Structure

```
studyPlanner/
├── main.py                 # FastAPI application (serves API & Frontend)
├── frontend/               # React + Vite TypeScript project
│   ├── src/
│   │   ├── components/     # UI Components (Dashboard, SubjectView, etc.)
│   │   ├── context/        # Global state (AppContext)
│   │   ├── services/       # API client (Axios)
│   │   └── types/          # TypeScript interfaces
│   └── dist/               # Compiled production build
├── src/                    # Backend source code
│   ├── api/                # API layer (Routers, Schemas)
│   ├── classifier/         # Rule-based content classification
│   ├── models/             # SQLAlchemy ORM models
│   ├── parsers/            # PDF/DOCX/PPT extraction logic
│   └── services/           # Business logic (Generation, Processing)
├── scripts/                # Database utility scripts
└── study_planner.db        # SQLite database
```

---

## 🔮 Roadmap

### Phase 3 (Upcoming)
- [ ] **Spaced Repetition**: Implement Leitner system for flashcards.
- [ ] **Interactive Timetable**: Drag-and-drop study scheduler.
- [ ] **AI/NLP Enhancement**: spaCy integration for better topic extraction.
- [ ] **Weak Topic Detection**: Analytics based on flashcard performance.
- [ ] **Export Options**: Export notes to Markdown/PDF.

---

## 🧪 Testing

### Run Processing Pipeline Test
```bash
python test_processing.py
```
*Tests registration, login, upload, processing, and resource retrieval.*

---

## 🤝 Contributing

This project demonstrates a full-stack AI-integrated application. Contributions are welcome!

---

**Built with ❤️ for students who want to study smarter, not harder.**
