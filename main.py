"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.config import get_settings
from src.database.base import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Initialize database
    print("Starting up Study Planner API...")
    init_db()
    yield
    # Shutdown
    print("Shutting down Study Planner API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered study planner that generates notes, cheatsheets, and personalized timetables",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "0.1.0"
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Study Planner API",
        "docs": "/docs",
        "health": "/health"
    }


# Import and include routers FIRST (before static files)
from src.api.routers import subjects, documents

app.include_router(subjects.router, prefix="/api", tags=["Subjects"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])

# Mount static files for frontend LAST (catch-all)
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
