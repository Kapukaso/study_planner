"""Seed database with sample data for testing."""
import sys
from pathlib import Path
from datetime import datetime, timedelta, date

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.base import SessionLocal
from src.models import (
    User, Subject, Chapter, Topic, TopicDependency,
    Note, Cheatsheet, PreviousYearQuestion, Flashcard,
    Timetable, TimetableSlot
)


def seed_data():
    """Seed the database with sample data."""
    db = SessionLocal()
    
    try:
        print("Seeding database with sample data...")
        print("=" * 50)
        
        # Create demo user
        user = User(
            email="demo@studyplanner.com",
            username="demo_user",
            password_hash="hashed_password_here",  # In production, use proper hashing
            full_name="Demo User",
            daily_study_hours=5.0,
            learning_style="visual"
        )
        db.add(user)
        db.flush()  # Get user ID
        print(f"[OK] Created user: {user.username}")
        
        # Create subject: Operating Systems
        subject = Subject(
            user_id=user.id,
            name="Operating Systems",
            code="CS301",
            exam_date=date.today() + timedelta(days=60),
            priority=9,
            total_marks=100
        )
        db.add(subject)
        db.flush()
        print(f"[OK] Created subject: {subject.name}")
        
        # Create Chapter 1: Process Management
        chapter1 = Chapter(
            subject_id=subject.id,
            title="Process Management",
            chapter_number=1,
            description="Introduction to processes and their management"
        )
        db.add(chapter1)
        db.flush()
        print(f"[OK] Created chapter: {chapter1.title}")
        
        # Create topics
        topic1 = Topic(
            chapter_id=chapter1.id,
            title="Process Concepts",
            description="Basic concepts of processes",
            difficulty="easy",
            difficulty_score=0.3,
            estimated_hours=2.0,
            importance_score=0.8,
            pyq_frequency=5,
            keywords=["process", "program", "state", "PCB"]
        )
        db.add(topic1)
        
        topic2 = Topic(
            chapter_id=chapter1.id,
            title="Process Synchronization",
            description="Synchronization mechanisms and critical section problem",
            difficulty="medium",
            difficulty_score=0.6,
            estimated_hours=4.0,
            importance_score=0.9,
            pyq_frequency=8,
            keywords=["synchronization", "mutex", "semaphore", "deadlock"]
        )
        db.add(topic2)
        
        topic3 = Topic(
            chapter_id=chapter1.id,
            title="Deadlock",
            description="Deadlock detection, prevention, and avoidance",
            difficulty="hard",
            difficulty_score=0.85,
            estimated_hours=5.0,
            importance_score=0.95,
            pyq_frequency=12,
            keywords=["deadlock", "resource allocation", "banker's algorithm"]
        )
        db.add(topic3)
        db.flush()
        print(f"[OK] Created topics: {topic1.title}, {topic2.title}, {topic3.title}")
        
        # Create topic dependency: Deadlock depends on Process Synchronization
        dependency = TopicDependency(
            topic_id=topic3.id,
            depends_on_topic_id=topic2.id,
            strength="required"
        )
        db.add(dependency)
        print(f"[OK] Created dependency: {topic3.title} -> {topic2.title}")
        
        # Create a note
        note = Note(
            topic_id=topic1.id,
            content="""# Process Concepts
            
## What is a Process?
- A program in execution
- Unit of work in modern operating systems
- Has its own address space, registers, and resources

## Process States
1. **New**: Process is being created
2. **Ready**: Process is waiting to be assigned to processor
3. **Running**: Instructions are being executed
4. **Waiting**: Process is waiting for some event
5. **Terminated**: Process has finished execution

## Process Control Block (PCB)
Contains:
- Process state
- Program counter
- CPU registers
- Memory management information
- Accounting information
            """,
            summary="Basic concepts of processes, states, and PCB",
            generation_method="manual"
        )
        db.add(note)
        print(f"[OK] Created note for: {topic1.title}")
        
        # Create a cheatsheet
        cheatsheet = Cheatsheet(
            topic_id=topic3.id,
            content="""# Deadlock Cheatsheet

## Four Necessary Conditions
1. Mutual Exclusion
2. Hold and Wait
3. No Preemption
4. Circular Wait

## Handling Methods
- **Prevention**: Negate one of the four conditions
- **Avoidance**: Use Banker's Algorithm
- **Detection**: Use resource allocation graph
- **Recovery**: Process termination or resource preemption
            """,
            formulas={
                "banker_algorithm": "Safe if: Available >= Need[i] for some i"
            },
            key_definitions={
                "deadlock": "A set of processes is in deadlock if each process is waiting for an event that can be caused only by another process in the set"
            },
            quick_tips=["Always study prevention vs avoidance", "Practice resource allocation graphs"]
        )
        db.add(cheatsheet)
        print(f"[OK] Created cheatsheet for: {topic3.title}")
        
        # Create previous year questions
        pyq1 = PreviousYearQuestion(
            topic_id=topic3.id,
            question_text="Explain the four necessary conditions for deadlock. Can deadlock occur if one of these conditions is not met?",
            answer_text="The four conditions are: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, 4) Circular Wait. Deadlock cannot occur if at least one condition is not met.",
            question_type="long_answer",
            marks=10,
            year=2023,
            source="End Semester Exam",
            difficulty="medium"
        )
        db.add(pyq1)
        
        pyq2 = PreviousYearQuestion(
            topic_id=topic2.id,
            question_text="What is a semaphore? Explain binary and counting semaphores.",
            question_type="short_answer",
            marks=5,
            year=2023,
            source="Mid Semester Exam",
            difficulty="easy"
        )
        db.add(pyq2)
        print(f"[OK] Created {2} previous year questions")
        
        # Create flashcards
        flashcard1 = Flashcard(
            topic_id=topic1.id,
            question="What is the difference between a process and a program?",
            answer="A program is passive (code stored on disk), while a process is active (program in execution with its own resources and state).",
            card_type="concept"
        )
        db.add(flashcard1)
        
        flashcard2 = Flashcard(
            topic_id=topic3.id,
            question="What are the four necessary conditions for deadlock?",
            answer="1. Mutual Exclusion\n2. Hold and Wait\n3. No Preemption\n4. Circular Wait",
            card_type="definition"
        )
        db.add(flashcard2)
        print(f"[OK] Created {2} flashcards")
        
        # Create a timetable
        timetable = Timetable(
            user_id=user.id,
            name="Operating Systems - 60 Day Plan",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=60),
            status="active",
            total_hours_allocated=50.0
        )
        db.add(timetable)
        db.flush()
        print(f"[OK] Created timetable: {timetable.name}")
        
        # Create timetable slots
        slot1 = TimetableSlot(
            timetable_id=timetable.id,
            topic_id=topic1.id,
            date=date.today() + timedelta(days=1),
            start_time=datetime.strptime("09:00", "%H:%M").time(),
            end_time=datetime.strptime("11:00", "%H:%M").time(),
            duration_hours=2.0,
            slot_type="study",
            status="pending"
        )
        db.add(slot1)
        
        slot2 = TimetableSlot(
            timetable_id=timetable.id,
            topic_id=topic2.id,
            date=date.today() + timedelta(days=2),
            start_time=datetime.strptime("14:00", "%H:%M").time(),
            end_time=datetime.strptime("18:00", "%H:%M").time(),
            duration_hours=4.0,
            slot_type="study",
            status="pending"
        )
        db.add(slot2)
        print(f"[OK] Created {2} timetable slots")
        
        # Commit all changes
        db.commit()
        print("=" * 50)
        print("[SUCCESS] Database seeded successfully!")
        print("\nSample data created:")
        print(f"  * 1 user (email: {user.email})")
        print(f"  * 1 subject ({subject.name})")
        print(f"  * 1 chapter ({chapter1.title})")
        print(f"  * 3 topics")
        print(f"  * 1 topic dependency")
        print(f"  * 1 note")
        print(f"  * 1 cheatsheet")
        print(f"  * 2 PYQs")
        print(f"  * 2 flashcards")
        print(f"  * 1 timetable with 2 slots")
        
    except Exception as e:
        db.rollback()
        print("=" * 50)
        print(f"[ERROR] Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
