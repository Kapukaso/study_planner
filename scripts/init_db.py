"""Database initialization script."""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.base import init_db


if __name__ == "__main__":
    print("Initializing database...")
    print("=" * 50)
    
    try:
        init_db()
        print("=" * 50)
        print("[SUCCESS] Database initialized successfully!")
        print("\nAll tables created:")
        print("  * users")
        print("  * subjects")
        print("  * documents")
        print("  * document_chunks")
        print("  * chapters")
        print("  * topics")
        print("  * topic_dependencies")
        print("  * notes")
        print("  * cheatsheets")
        print("  * pyqs")
        print("  * flashcards")
        print("  * timetables")
        print("  * timetable_slots")
        print("  * user_progress")
        
    except Exception as e:
        print("=" * 50)
        print(f"[ERROR] Error initializing database: {e}")
        sys.exit(1)
