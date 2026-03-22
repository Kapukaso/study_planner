# 🎓 Study Planner: AI-Powered Learning Ecosystem

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)

An intelligent educational platform that transforms raw study materials into a structured knowledge base. Upload your PDFs, Word documents, or PowerPoints, and watch as the system automatically generates comprehensive notes, interactive flashcards, cheatsheets, and a personalized study timetable.

---

## ✨ Key Features

### 📂 Intelligent Document Ingestion
- **Multi-Format Support**: Seamlessly process PDF, DOCX, PPTX, and Image files.
- **OCR Integration**: Built-in Tesseract OCR support for scanned documents and images.
- **Structural Parsing**: Preserves document hierarchy, slide titles, and table structures.

### 🧠 Content Classification Engine
- **Automated Chunking**: Intelligently segments long documents into manageable text chunks using structural markers.
- **Priority-Based Labeling**: Employs a deterministic classification hierarchy:
  1. 📐 **Formulas**: Identified via mathematical symbols (`=`, `+`, `Σ`, etc.) and variable relationships.
  2. 📖 **Definitions**: Extracted using linguistic patterns (e.g., *"X is defined as Y"*, *"X refers to Y"*).
  3. ❓ **PYQs**: Detected through examination-specific keywords and year markers (e.g., *"2023"*, *"10 Marks"*).
  4. 💡 **Examples**: Isolated through contextual triggers like *"For instance"*, *"Consider a scenario"*.
  5. ⭐ **Highlights**: Critical information tagged by emphasis markers and bold text.
  6. 📝 **Concepts**: Default classification for foundational theoretical content.

### 🛠️ Resource Generation Logic
- **Regex-Powered Flashcards**: Automatically transforms definitions and formulas into Q&A pairs by splitting text on linguistic pivots (e.g., *"is"*, *"means"*, *"="*).
- **Extractive Notes**: Compiles high-confidence chunks into structured Markdown notes, preserving the original pedagogical flow.
- **Smart PYQ Extraction**: Parses year and mark information from question text to help prioritize exam preparation.
- **Automated Cheatsheets**: Aggregates all extracted formulas and key definitions into a condensed, one-page summary for rapid review.

### 📅 Personalized Study Planning
- **Automated Timetables**: Generates optimized study schedules based on exam dates and subject priority.
- **Difficulty Estimation**: Calculates study time requirements using content complexity and topic length.
- **Progress Tracking**: Monitor your mastery across subjects, chapters, and topics.

---

## 🏗️ System Architecture

### Subsystems
1.  **Document Parser**: Multi-threaded extraction engine (PDF/Word/PPT).
2.  **Content Classifier**: Rule-based + ML hybrid system for text categorization.
3.  **Knowledge Extractor**: Maps dependencies and structures topics into a hierarchy.
4.  **Resource Generator**: Compiles classified chunks into study materials.
5.  **Planner Engine**: Constraint-based scheduler for timetable generation.

### Database Schema (14 Interconnected Tables)
- **Core**: `users`, `subjects`, `chapters`, `topics`
- **Processing**: `documents`, `document_chunks`
- **Resources**: `notes`, `cheatsheets`, `pyqs`, `flashcards`
- **Planning**: `timetables`, `timetable_slots`, `user_progress`, `topic_dependencies`

---

## 🛠️ Tech Stack

### Backend (Python 3.12+)
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance async API)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Modern data modeling)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/) (Strict type safety)
- **Security**: [JWT](https://jwt.io/) (Secure authentication)
- **Parsing**: `pdfplumber`, `python-docx`, `python-pptx`, `pytesseract`

### Frontend (React 18)
- **Framework**: [React](https://reactjs.org/) + [Vite](https://vitejs.dev/) + [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) (Modern dark-themed Glassmorphism UI)
- **Icons**: [Lucide React](https://lucide.dev/)
- **API Client**: [Axios](https://axios-http.com/)

### Infrastructure
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **API Documentation**: Swagger UI (`/docs`) & ReDoc (`/redoc`)

---

## 📁 Project Structure

```bash
studyPlanner/
├── main.py                 # FastAPI Application entry point
├── src/                    # Backend Source Code
│   ├── api/                # API Layer (Routers, Schemas, Dependencies)
│   ├── classifier/         # Content classification logic & patterns
│   ├── models/             # SQLAlchemy Data Models (14 tables)
│   ├── parsers/            # Specialized Document Parsers (PDF/DOCX/PPT)
│   ├── services/           # Business Logic (Generation, Processing, Planning)
│   ├── database/           # Database initialization & seeding scripts
│   └── utils/              # File storage & common utilities
├── frontend/               # Modern React + TypeScript Frontend
│   ├── src/
│   │   ├── components/     # UI Components (Dashboard, SubjectView, etc.)
│   │   ├── context/        # Global State Management (AppContext)
│   │   ├── services/       # API Integration Layer
│   │   └── types/          # TypeScript Interfaces
│   └── public/             # Static Assets
├── scripts/                # Database management utility scripts
└── uploads/                # Local storage for processed documents
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Tesseract OCR** (Optional, for image processing)

### 1. Backend Setup
```bash
# Clone the repository
git clone <repo-url>
cd studyPlanner

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize and seed the database
python scripts/init_db.py
python scripts/seed_db.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run build
```

### 3. Run the Application
```bash
# From the root directory
uvicorn main:app --reload
```
- **API Base**: `http://localhost:8000`
- **Frontend**: Served automatically at `http://localhost:8000`
- **Swagger Docs**: `http://localhost:8000/docs`

---

## 🧪 Testing
The project includes automated tests for the core processing pipeline and parsers.
```bash
# Test Document Processing
python test_processing.py

# Test Document Parsers (PDF/DOCX/PPT)
python test_parsers.py

# Test API Endpoints
python test_api.py
```

---

## 🔮 Roadmap
- [ ] **Phase 3**: Advanced AI integration with spaCy/Transformers for semantic topic extraction.
- [ ] **Spaced Repetition**: Implement Leitner system algorithms for flashcard scheduling.
- [ ] **Adaptive Planner**: Real-time timetable rescheduling based on user performance.
- [ ] **Vector Search**: Semantic document search using vector embeddings.
- [ ] **Export Suite**: Export study resources to PDF, Markdown, and Notion.

---

**Built with ❤️ for a smarter way to learn.**
