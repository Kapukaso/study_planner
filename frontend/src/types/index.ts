export interface Subject {
  id: string;
  name: string;
  code?: string;
  exam_date?: string;
  priority: number;
  total_marks?: number;
  created_at: string;
  updated_at: string;
  chapters_count: number;
  topics_count: number;
  documents_count: number;
}

export interface Topic {
  id: string;
  chapter_id: string;
  title: string;
  description?: string;
  difficulty?: string;
  difficulty_score?: number;
  estimated_hours?: number;
  importance_score?: number;
  pyq_frequency?: number;
  keywords?: string[];
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: string;
  subject_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  processing_status: 'pending' | 'processing' | 'completed' | 'failed';
  page_count?: number;
  uploaded_at: string;
  processed_at?: string;
}

export interface Note {
  id: string;
  topic_id: string;
  content: string;
  summary?: string;
  examples?: string[];
  generation_method?: string;
  version: number;
  created_at: string;
  updated_at: string;
}

export interface Flashcard {
  id: string;
  topic_id: string;
  question: string;
  answer: string;
  card_type?: string;
  created_at: string;
}

export interface PYQ {
  id: string;
  topic_id: string;
  question_text: string;
  answer_text?: string;
  question_type?: string;
  marks?: number;
  year?: number;
  source?: string;
  difficulty?: string;
  created_at: string;
}

export interface TopicResources {
  topic_id: string;
  notes: Note[];
  flashcards: Flashcard[];
  pyqs: PYQ[];
  cheatsheets: any[]; // Add Cheatsheet type if needed
}
