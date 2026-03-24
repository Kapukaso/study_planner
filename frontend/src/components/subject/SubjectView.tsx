import React, { useState, useEffect } from 'react';
import { ArrowLeft, BookOpen, FileText, Brain, HelpCircle } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import api from '../../services/api';
import type { Topic, TopicResources } from '../../types';
import { cn } from '../../lib/utils';
import Button from '../common/Button';
import Card from '../common/Card';
import Badge from '../common/Badge';
import EmptyState from '../common/EmptyState';

const SubjectView: React.FC = () => {
  const { currentSubject, setCurrentSubject } = useAppContext();
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<string | null>(null);
  const [resources, setResources] = useState<TopicResources | null>(null);
  const [activeTab, setActiveTab] = useState<'docs' | 'notes' | 'flashcards' | 'pyqs'>('docs');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (currentSubject) {
      fetchTopics();
    }
  }, [currentSubject]);

  useEffect(() => {
    if (selectedTopicId) {
      fetchResources(selectedTopicId);
    }
  }, [selectedTopicId]);

  const fetchTopics = async () => {
    try {
      const response = await api.get(`/api/subjects/${currentSubject?.id}/topics`);
      const fetchedTopics = response.data.topics || [];
      setTopics(fetchedTopics);
      if (fetchedTopics.length > 0) {
        setSelectedTopicId(fetchedTopics[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch topics:', error);
    }
  };

  const fetchResources = async (topicId: string) => {
    setLoading(true);
    try {
      const response = await api.get(`/api/topics/${topicId}/resources`);
      setResources(response.data);
    } catch (error) {
      console.error('Failed to fetch resources:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!currentSubject) return null;

  return (
    <div className="flex flex-col h-full animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => setCurrentSubject(null)}
          className="p-2 hover:bg-white/5 rounded-full transition-colors text-slate-400 hover:text-white"
        >
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div>
          <h2 className="text-3xl font-bold text-white">{currentSubject.name}</h2>
          <p className="text-slate-500 font-medium">{currentSubject.code || 'No Code'}</p>
        </div>
      </div>

      <div className="grid grid-cols-[300px_1fr] gap-8 flex-1 overflow-hidden">
        {/* Topics Sidebar */}
        <Card variant="glass" className="flex flex-col overflow-hidden p-6" isHoverable={false}>
          <h3 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4 flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            Topics
          </h3>
          <div className="flex-1 overflow-y-auto space-y-2 pr-2 custom-scrollbar">
            {topics.length === 0 ? (
              <p className="text-slate-600 text-sm italic">No topics generated yet. Upload documents to get started.</p>
            ) : (
              topics.map(topic => (
                <button
                  key={topic.id}
                  onClick={() => setSelectedTopicId(topic.id)}
                  className={cn(
                    "w-full text-left p-4 rounded-2xl transition-all duration-200 group relative overflow-hidden",
                    selectedTopicId === topic.id 
                      ? "bg-indigo-600 text-white shadow-lg shadow-indigo-500/20" 
                      : "text-slate-400 hover:bg-white/5 hover:text-slate-200"
                  )}
                >
                  <span className="relative z-10 font-semibold text-sm line-clamp-2">{topic.title}</span>
                  {topic.difficulty && (
                    <Badge 
                      variant={selectedTopicId === topic.id ? "primary" : "cyan"}
                      size="xs"
                      className="mt-2"
                    >
                      {topic.difficulty}
                    </Badge>
                  )}
                </button>
              ))
            )}
          </div>
        </Card>

        {/* Content Area */}
        <Card variant="glass" className="flex flex-col overflow-hidden p-0" isHoverable={false}>
          {/* Tabs */}
          <div className="flex p-2 gap-2 border-b border-white/5 bg-slate-950/20">
            {[
              { id: 'docs', label: 'Documents', icon: FileText },
              { id: 'notes', label: 'Notes', icon: BookOpen },
              { id: 'flashcards', label: 'Flashcards', icon: Brain },
              { id: 'pyqs', label: 'PYQs', icon: HelpCircle },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={cn(
                  "flex items-center gap-2 px-6 py-3 rounded-2xl font-bold text-sm transition-all",
                  activeTab === tab.id 
                    ? "bg-white/10 text-white shadow-inner" 
                    : "text-slate-500 hover:text-slate-300 hover:bg-white/5"
                )}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
            {loading ? (
              <div className="flex flex-col items-center justify-center h-full gap-4 text-slate-500">
                <div className="w-8 h-8 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
                <p className="font-medium animate-pulse">Analyzing content...</p>
              </div>
            ) : (
              <div className="animate-in fade-in duration-300">
                {activeTab === 'docs' && (
                  <div className="space-y-4">
                    <div className="border-2 border-dashed border-white/10 rounded-3xl p-12 text-center hover:border-indigo-500/50 transition-colors group cursor-pointer">
                      <div className="w-16 h-16 bg-indigo-500/10 rounded-2xl flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
                        <FileText className="w-8 h-8 text-indigo-400" />
                      </div>
                      <h4 className="text-xl font-bold text-slate-200">Upload Knowledge</h4>
                      <p className="text-slate-500 max-w-xs mx-auto mt-2">Drag and drop your PDF or DOCX files here to generate study materials.</p>
                    </div>
                  </div>
                )}

                {activeTab === 'notes' && (
                  <div className="space-y-6">
                    {resources?.notes.map(note => (
                      <div key={note.id} className="prose prose-invert max-w-none prose-indigo">
                        <Card variant="outline" className="p-8 leading-relaxed text-slate-200 whitespace-pre-wrap">
                          {note.content}
                        </Card>
                      </div>
                    ))}
                    {(!resources?.notes || resources.notes.length === 0) && (
                      <EmptyState message="No notes available for this topic yet." />
                    )}
                  </div>
                )}

                {activeTab === 'flashcards' && (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {resources?.flashcards.map(card => (
                      <Flashcard key={card.id} card={card} />
                    ))}
                    {(!resources?.flashcards || resources.flashcards.length === 0) && (
                      <EmptyState message="No flashcards available for this topic yet." />
                    )}
                  </div>
                )}

                {activeTab === 'pyqs' && (
                  <div className="space-y-4">
                    {resources?.pyqs.map(pyq => (
                      <Card key={pyq.id} variant="outline" className="hover:border-pink-500/30 transition-colors">
                        <div className="flex justify-between items-start mb-4">
                          <Badge variant="pink" size="xs">
                            PYQ {pyq.year}
                          </Badge>
                          {pyq.marks && (
                            <span className="text-slate-500 text-xs font-bold">{pyq.marks} Marks</span>
                          )}
                        </div>
                        <p className="text-slate-200 font-medium leading-relaxed">{pyq.question_text}</p>
                      </Card>
                    ))}
                    {(!resources?.pyqs || resources.pyqs.length === 0) && (
                      <EmptyState message="No previous year questions found for this topic." />
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};

const Flashcard: React.FC<{ card: any }> = ({ card }) => {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div 
      onClick={() => setIsFlipped(!isFlipped)}
      className="h-72 cursor-pointer perspective-1000 group"
    >
      <div className={cn(
        "relative w-full h-full transition-all duration-700 preserve-3d",
        isFlipped ? "rotate-y-180" : ""
      )}>
        {/* Front */}
        <Card className="absolute inset-0 backface-hidden rounded-[32px] p-10 flex flex-col items-center justify-center text-center shadow-2xl" isHoverable={true}>
          <span className="text-[10px] font-black text-indigo-400 uppercase tracking-[0.2em] mb-4">Question</span>
          <p className="text-xl font-bold text-white leading-relaxed line-clamp-4">{card.question}</p>
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-all duration-500 translate-y-2 group-hover:translate-y-0">
            <Badge variant="primary" size="xs">Tap to flip</Badge>
          </div>
        </Card>
        {/* Back */}
        <div className="absolute inset-0 backface-hidden rotate-y-180 bg-gradient-to-br from-indigo-600 to-violet-700 rounded-[32px] p-10 flex flex-col items-center justify-center text-center shadow-2xl shadow-indigo-500/40">
          <span className="text-[10px] font-black text-white/50 uppercase tracking-[0.2em] mb-4">Answer</span>
          <p className="text-white text-lg font-bold leading-relaxed">{card.answer}</p>
        </div>
      </div>
    </div>
  );
};

export default SubjectView;
