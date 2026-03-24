"""Resource generation service - auto-generates study materials from chunks."""
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
import uuid
import re
import spacy

from src.models import (
    Document, DocumentChunk, Topic, Chapter, Subject,
    Note, Flashcard, PreviousYearQuestion, Cheatsheet
)

logger = logging.getLogger(__name__)


class ResourceGenerator:
    """Generates study resources (notes, flashcards, etc.) from document chunks."""

    def __init__(self, db: Session):
        self.db = db
        # Load spaCy for advanced text extraction
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

    def generate_resources_for_document(self, document_id: str) -> dict:
        """
        Generate all types of resources for a document.
        
        Args:
            document_id: ID of the document to process
            
        Returns:
            Dictionary with counts of generated resources
        """
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise ValueError(f"Document {document_id} not found")

        # Get all chunks for this document
        chunks = self.db.query(DocumentChunk).filter(
            DocumentChunk.document_id == document_id
        ).order_by(DocumentChunk.chunk_index).all()

        if not chunks:
            return {"notes": 0, "flashcards": 0, "pyqs": 0, "cheatsheets": 0}

        # For now, we'll use a default topic for the entire document if no chapters exist
        # In a real scenario, we'd use classification or headings to split into topics
        topic = self._get_or_create_default_topic(document)

        results = {
            "notes": self._generate_notes(topic, chunks),
            "flashcards": self._generate_flashcards(topic, chunks),
            "pyqs": self._generate_pyqs(topic, chunks),
            "cheatsheets": self._generate_cheatsheet(topic, chunks)
        }

        return results

    def _get_or_create_default_topic(self, document: Document) -> Topic:
        """Get or create a default topic for the document."""
        # Try to find an existing chapter for this subject
        chapter = self.db.query(Chapter).filter(
            Chapter.subject_id == document.subject_id
        ).first()

        if not chapter:
            # Create a default chapter
            chapter = Chapter(
                subject_id=document.subject_id,
                title=f"General - {document.filename}",
                chapter_number=1
            )
            self.db.add(chapter)
            self.db.commit()
            self.db.refresh(chapter)

        # Try to find an existing topic in this chapter
        topic = self.db.query(Topic).filter(
            Topic.chapter_id == chapter.id,
            Topic.title == "Main Content"
        ).first()

        if not topic:
            # Create a default topic
            topic = Topic(
                chapter_id=chapter.id,
                title="Main Content",
                description=f"Auto-generated content from {document.filename}",
                difficulty="medium"
            )
            self.db.add(topic)
            self.db.commit()
            self.db.refresh(topic)

        return topic

    def _generate_notes(self, topic: Topic, chunks: List[DocumentChunk]) -> int:
        """Generate structured markdown notes grouped by content type."""
        existing_note = self.db.query(Note).filter(Note.topic_id == topic.id).first()
        if existing_note:
            return 0

        # Organize chunks by their semantic classification
        categorized_content = {
            'concept': [],
            'definition': [],
            'formula': [],
            'example': [],
            'highlight': [],
            'summary': []
        }

        extracted_examples = []
        
        for chunk in chunks:
            c_type = chunk.content_type
            if c_type in categorized_content:
                categorized_content[c_type].append(chunk.raw_text)
            
            if c_type == 'example':
                extracted_examples.append(chunk.raw_text)

        # Build a beautiful Markdown Note
        markdown_sections = []
        
        if categorized_content['summary'] or categorized_content['highlight']:
            markdown_sections.append("## 📌 Key Takeaways")
            markdown_sections.extend([f"- {text}" for text in categorized_content['highlight']])
            markdown_sections.extend([f"> {text}" for text in categorized_content['summary']])
            
        if categorized_content['concept']:
            markdown_sections.append("## 🧠 Core Concepts")
            markdown_sections.extend([f"{text}\n" for text in categorized_content['concept']])
            
        if categorized_content['definition']:
            markdown_sections.append("## 📖 Definitions")
            for text in categorized_content['definition']:
                # Bold the term if it follows a "Term: definition" pattern
                formatted = re.sub(r'^([^:]+):', r'**\1**:', text)
                markdown_sections.append(f"- {formatted}")
                
        if categorized_content['formula']:
            markdown_sections.append("## 🧮 Formulas")
            markdown_sections.extend([f"`{text}`" for text in categorized_content['formula']])

        full_content = "\n\n".join(markdown_sections)
        
        # Fallback if categories were empty
        if not full_content.strip():
            full_content = "\n\n".join([c.raw_text for c in chunks])

        note = Note(
            topic_id=topic.id,
            content=full_content,
            summary=categorized_content['summary'][0][:200] + "..." if categorized_content['summary'] else "Auto-generated structured notes.",
            examples=extracted_examples,
            generation_method="ml_extraction"
        )
        
        self.db.add(note)
        self.db.commit()
        return 1

    def _generate_flashcards(self, topic: Topic, chunks: List[DocumentChunk]) -> int:
        """Generate smart flashcards using NLP (spaCy) for definitions and formulas."""
        count = 0
        for chunk in chunks:
            if chunk.content_type in ['definition', 'formula', 'concept']:
                text = chunk.raw_text
                question = ""
                answer = ""

                if chunk.content_type == 'definition':
                    # 1. Try Regex first
                    match = re.search(r'^([^:]+):', text)
                    if match:
                        question = match.group(1).strip()
                        answer = text[match.end():].strip()
                    else:
                        # 2. Use spaCy to find the Subject and Object
                        doc = self.nlp(text)
                        for token in doc:
                            if token.lemma_ in ["be", "mean", "define", "refer"]:
                                lefts = list(token.lefts)
                                rights = list(token.rights)
                                if lefts and rights:
                                    subject = " ".join([w.text for w in lefts[0].subtree])
                                    question = f"What is meant by {subject}?"
                                    answer = text
                                    break

                elif chunk.content_type == 'formula':
                    if '=' in text:
                        parts = text.split('=', 1)
                        question = f"What is the formula for: {parts[0].strip()}?"
                        answer = text.strip()
                        
                elif chunk.content_type == 'concept':
                    # Extract Key Entities using spaCy for fill-in-the-blank cards
                    doc = self.nlp(text)
                    if doc.ents:
                        # Pick the most prominent entity
                        entity = doc.ents[0]
                        if len(entity.text) > 3:
                            question = text.replace(entity.text, "______", 1)
                            answer = entity.text

                if question and answer and len(question) > 5 and len(answer) > 2:
                    exists = self.db.query(Flashcard).filter(
                        Flashcard.topic_id == topic.id,
                        Flashcard.question == question
                    ).first()
                    
                    if not exists:
                        flashcard = Flashcard(
                            topic_id=topic.id,
                            question=question,
                            answer=answer,
                            card_type=chunk.content_type
                        )
                        self.db.add(flashcard)
                        count += 1
        
        if count > 0:
            self.db.commit()
        return count

    def _generate_pyqs(self, topic: Topic, chunks: List[DocumentChunk]) -> int:
        """Extract previous year questions."""
        count = 0
        for chunk in chunks:
            if chunk.content_type == 'pyq':
                # Try to extract year and marks
                text = chunk.raw_text
                year_match = re.search(r'\b(20[1-2]\d)\b', text)
                marks_match = re.search(r'\((\d+)\s*(marks|M|m)\)', text)
                
                year = int(year_match.group(1)) if year_match else None
                marks = int(marks_match.group(1)) if marks_match else None

                # Check if already exists
                exists = self.db.query(PreviousYearQuestion).filter(
                    PreviousYearQuestion.topic_id == topic.id,
                    PreviousYearQuestion.question_text == text
                ).first()

                if not exists:
                    pyq = PreviousYearQuestion(
                        topic_id=topic.id,
                        question_text=text,
                        year=year,
                        marks=marks,
                        question_type="unknown",
                        difficulty="medium"
                    )
                    self.db.add(pyq)
                    count += 1
        
        if count > 0:
            self.db.commit()
        return count

    def _generate_cheatsheet(self, topic: Topic, chunks: List[DocumentChunk]) -> int:
        """Generate a cheatsheet summary."""
        # Check if cheatsheet already exists
        existing = self.db.query(Cheatsheet).filter(Cheatsheet.topic_id == topic.id).first()
        if existing:
            return 0

        formulas = []
        definitions = []
        
        for chunk in chunks:
            if chunk.content_type == 'formula':
                formulas.append(chunk.raw_text)
            elif chunk.content_type == 'definition':
                definitions.append(chunk.raw_text)

        if not formulas and not definitions:
            return 0

        cheatsheet = Cheatsheet(
            topic_id=topic.id,
            content=f"# Cheatsheet: {topic.title}\n\nAuto-generated summary.",
            formulas=formulas,
            key_definitions=definitions,
            format="markdown"
        )
        
        self.db.add(cheatsheet)
        self.db.commit()
        return 1

