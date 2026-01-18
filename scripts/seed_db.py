"""Seed database script - wrapper to run from project root."""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.seed import seed_data

if __name__ == "__main__":
    seed_data()
