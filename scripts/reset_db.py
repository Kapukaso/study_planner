"""Database reset script for development."""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.base import Base, engine
from src.database.seed import seed_data


if __name__ == "__main__":
    print("Resetting database...")
    print("=" * 50)
    print("[WARNING] This will DELETE all existing data!")
    print("=" * 50)
    
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() != "yes":
        print("Operation cancelled.")
        sys.exit(0)
    
    try:
        # Drop all tables
        print("\n[DROPPPING] Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("[OK] All tables dropped")
        
        # Recreate all tables
        print("\n[CREATING] Creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("[OK] All tables created")
        
        # Seed data
        print("\n[SEEDING] Seeding data...")
        seed_data()
        
        print("\n" + "=" * 50)
        print("[SUCCESS] Database reset complete!")
        
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"[ERROR] Error resetting database: {e}")
        sys.exit(1)
