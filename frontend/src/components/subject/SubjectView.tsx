import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, BookOpen, FileText, Brain, HelpCircle } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import api from '../../services/api';
import type { Topic, TopicResources, Subject } from '../../types';
import { cn } from '../../lib/utils';
import Badge from '../common/Badge';
import EmptyState from '../common/EmptyState';

const SubjectView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { subjects, loading: subjectsLoading } = useAppContext();
  
  const [subject, setSubject] = useState<Subject | null>(null);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedTopicId, setSelectedTopicId] = useState<string | null>(null);
  const [resources, setResources] = useState<TopicResources | null>(null);
  const [activeTab, setActiveTab] = useState<'docs' | 'notes' | 'flashcards' | 'pyqs'>('docs');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (id && subjects.length > 0) {
      const foundSubject = subjects.find(s => s.id === id);
      if (foundSubject) {
        setSubject(foundSubject);
      } else {
        // Fallback: try to fetch individual subject if not in list
        fetchSubject(id);
      }
    }
  }, [id, subjects]);

  useEffect(() => {
    if (subject) {
      fetchTopics();
    }
  }, [subject]);

  useEffect(() => {
    if (selectedTopicId) {
      fetchResources(selectedTopicId);
    }
  }, [selectedTopicId]);

  const fetchSubject = async (subjectId: string) => {
    try {
      const response = await api.get(`/api/subjects/${subjectId}`);
      setSubject(response.data);
    } catch (error) {
      console.error('Failed to fetch subject:', error);
      navigate('/');
    }
  };

  const fetchTopics = async () => {
    if (!subject) return;
    try {
      const response = await api.get(`/api/subjects/${subject.id}/topics`);
      const fetchedTopics = response.data.topics || [];
      setTopics(fetchedTopics);
      if (fetchedTopics.length > 0 && !selectedTopicId) {
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

  if (subjectsLoading && !subject) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="w-12 h-12 border-t-2 border-cyan-500 rounded-full animate-spin shadow-[0_0_15px_rgba(0,245,255,0.4)]" />
      </div>
    );
  }

  if (!subject) return null;

  return (
    <div className="flex flex-col h-full animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-7xl mx-auto">
      <div className="flex items-center gap-6 mb-12 group">
        <button 
          onClick={() => navigate('/')}
          className="p-4 bg-white/5 hover:bg-cyan-500 hover:text-black rounded-2xl transition-all duration-300 text-slate-400 shadow-lg active:scale-95"
        >
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div>
          <h2 className="text-5xl font-black text-white tracking-tight leading-none mb-2">{subject.name}</h2>
          <div className="flex items-center gap-3">
            <span className="text-[10px] font-black uppercase tracking-[0.3em] text-cyan-400 bg-cyan-400/10 px-3 py-1 rounded-lg border border-cyan-400/20">
              {subject.code || 'UNIT-ALPHA'}
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-800" />
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Neural Link Established</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-[340px_1fr] gap-10 flex-1 overflow-hidden">
        {/* Topics Sidebar */}
        <div className="flex flex-col overflow-hidden space-y-6">
          <div className="glass-morphism rounded-[32px] border border-white/5 flex flex-col overflow-hidden h-full shadow-2xl">
            <div className="p-8 border-b border-white/5">
              <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.25em] flex items-center gap-3">
                <BookOpen className="w-4 h-4 text-cyan-400" />
                Knowledge Nodes
              </h3>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-2 custom-scrollbar">
              {topics.length === 0 ? (
                <div className="p-8 text-center space-y-4">
                  <div className="w-12 h-12 bg-white/5 rounded-2xl flex items-center justify-center mx-auto opacity-20">
                    <Brain className="w-6 h-6" />
                  </div>
                  <p className="text-slate-600 text-xs font-bold uppercase tracking-widest leading-relaxed">No nodes detected. Upload core documents.</p>
                </div>
              ) : (
                topics.map(topic => (
                  <button
                    key={topic.id}
                    onClick={() => setSelectedTopicId(topic.id)}
                    className={cn(
                      "w-full text-left p-5 rounded-2xl transition-all duration-500 group relative overflow-hidden",
                      selectedTopicId === topic.id 
                        ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-[0_0_25px_rgba(0,245,255,0.1)]" 
                        : "text-slate-500 hover:bg-white/[0.03] hover:text-slate-200 border border-transparent"
                    )}
                  >
                    {selectedTopicId === topic.id && (
                      <span className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-6 bg-cyan-400 rounded-r-full shadow-[0_0_12px_rgba(0,245,255,0.6)]" />
                    )}
                    <span className="relative z-10 font-black text-xs uppercase tracking-widest line-clamp-2 block mb-2">{topic.title}</span>
                    {topic.difficulty && (
                      <Badge 
                        variant={selectedTopicId === topic.id ? "cyan" : "outline"}
                        size="xs"
                        className="font-black"
                      >
                        {topic.difficulty}
                      </Badge>
                    )}
                  </button>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="glass-morphism rounded-[32px] border border-white/5 flex flex-col overflow-hidden shadow-2xl relative">
          <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 blur-[100px] pointer-events-none" />
          
          {/* Tabs */}
          <div className="flex p-4 gap-4 border-b border-white/5 bg-white/[0.01] overflow-x-auto no-scrollbar">
            {[
              { id: 'docs', label: 'Telemetry', icon: FileText },
              { id: 'notes', label: 'Synthesis', icon: BookOpen },
              { id: 'flashcards', label: 'Neural Flash', icon: Brain },
              { id: 'pyqs', label: 'History', icon: HelpCircle },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={cn(
                  "flex items-center gap-3 px-8 py-4 rounded-2xl font-black text-[10px] uppercase tracking-[0.25em] transition-all whitespace-nowrap group",
                  activeTab === tab.id 
                    ? "bg-white text-black shadow-[0_8px_24px_rgba(255,255,255,0.2)]" 
                    : "text-slate-500 hover:text-slate-200 hover:bg-white/5"
                )}
              >
                <tab.icon className={cn("w-4 h-4 transition-transform group-hover:scale-110", activeTab === tab.id ? "text-black" : "text-cyan-400/60")} />
                {tab.label}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-y-auto p-10 custom-scrollbar relative z-10">
            {loading ? (
              <div className="flex flex-col items-center justify-center h-full gap-6">
                <div className="relative">
                  <div className="w-16 h-16 border-2 border-cyan-500/20 border-t-cyan-500 rounded-full animate-spin shadow-[0_0_30px_rgba(0,245,255,0.2)]" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-8 h-8 bg-cyan-500/10 rounded-full animate-pulse" />
                  </div>
                </div>
                <p className="text-xs font-black text-cyan-400 uppercase tracking-[0.4em] animate-pulse">Neural Reconstruction...</p>
              </div>
            ) : (
              <div className="animate-in fade-in duration-700">
                {activeTab === 'docs' && (
                  <div className="space-y-6">
                    <div className="border-2 border-dashed border-white/5 rounded-[40px] p-20 text-center hover:border-cyan-500/30 transition-all duration-500 group cursor-pointer bg-white/[0.01] hover:bg-cyan-500/[0.02]">
                      <div className="w-20 h-20 bg-gradient-to-br from-cyan-400/20 to-blue-600/20 rounded-3xl flex items-center justify-center mx-auto mb-8 group-hover:scale-110 group-hover:rotate-3 transition-all shadow-xl">
                        <FileText className="w-10 h-10 text-cyan-400" />
                      </div>
                      <h4 className="text-2xl font-black text-white tracking-tight mb-3">Sync Knowledge Base</h4>
                      <p className="text-slate-500 font-bold max-w-sm mx-auto leading-relaxed">Drag and drop academic artifacts to initiate neural extraction.</p>
                      <button className="mt-8 px-10 py-4 bg-white text-black rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-cyan-400 transition-colors shadow-lg">Browse Files</button>
                    </div>
                  </div>
                )}

                {activeTab === 'notes' && (
                  <div className="space-y-8">
                    {resources?.notes.map(note => (
                      <div key={note.id} className="prose prose-invert max-w-none">
                        <div className="glass-morphism border border-white/5 p-10 rounded-[32px] leading-relaxed text-slate-200 whitespace-pre-wrap font-medium text-lg shadow-xl relative overflow-hidden group">
                          <div className="absolute top-0 left-0 w-1.5 h-full bg-cyan-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                          {note.content}
                        </div>
                      </div>
                    ))}
                    {(!resources?.notes || resources.notes.length === 0) && (
                      <EmptyState message="No synthesis records found for this node." />
                    )}
                  </div>
                )}

                {activeTab === 'flashcards' && (
                  <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
                    {resources?.flashcards.map(card => (
                      <Flashcard key={card.id} card={card} />
                    ))}
                    {(!resources?.flashcards || resources.flashcards.length === 0) && (
                      <div className="col-span-full py-20">
                        <EmptyState message="No active recall patterns generated." />
                      </div>
                    )}
                  </div>
                )}

                {activeTab === 'pyqs' && (
                  <div className="space-y-6">
                    {resources?.pyqs.map(pyq => (
                      <div key={pyq.id} className="glass-morphism border border-white/5 p-8 rounded-[32px] hover:border-purple-500/30 transition-all duration-500 shadow-lg relative group">
                        <div className="flex justify-between items-center mb-6">
                          <div className="flex items-center gap-3">
                            <Badge variant="purple" size="xs" className="font-black px-3 py-1">
                              LEGACY DATA {pyq.year}
                            </Badge>
                            {pyq.difficulty && (
                              <Badge variant="outline" size="xs" className="text-slate-500 border-slate-800">
                                {pyq.difficulty}
                              </Badge>
                            )}
                          </div>
                          {pyq.marks && (
                            <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest bg-white/5 px-3 py-1 rounded-lg border border-white/5">{pyq.marks} Credits</span>
                          )}
                        </div>
                        <p className="text-white font-black text-xl leading-relaxed tracking-tight group-hover:text-purple-400 transition-colors">{pyq.question_text}</p>
                      </div>
                    ))}
                    {(!resources?.pyqs || resources.pyqs.length === 0) && (
                      <EmptyState message="No historical exam patterns detected." />
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const Flashcard: React.FC<{ card: any }> = ({ card }) => {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div 
      onClick={() => setIsFlipped(!isFlipped)}
      className="h-80 cursor-pointer perspective-2000 group"
    >
      <div className={cn(
        "relative w-full h-full transition-all duration-1000 preserve-3d shadow-2xl rounded-[40px]",
        isFlipped ? "rotate-y-180" : ""
      )}>
        {/* Front */}
        <div className="absolute inset-0 backface-hidden glass-morphism border border-white/5 rounded-[40px] p-12 flex flex-col items-center justify-center text-center group-hover:bg-white/[0.04] transition-colors overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-400/5 blur-3xl rounded-full -mr-16 -mt-16" />
          <span className="text-[10px] font-black text-cyan-400 uppercase tracking-[0.4em] mb-6">Inquiry Node</span>
          <p className="text-2xl font-black text-white leading-tight tracking-tight line-clamp-4">{card.question}</p>
          <div className="mt-8">
            <Badge variant="outline" size="xs" className="text-slate-600 border-slate-800 uppercase font-black tracking-widest">Tap to reveal</Badge>
          </div>
        </div>
        {/* Back */}
        <div className="absolute inset-0 backface-hidden rotate-y-180 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-[40px] p-12 flex flex-col items-center justify-center text-center shadow-[0_0_50px_rgba(0,245,255,0.3)]">
          <div className="absolute inset-0 bg-black/10 mix-blend-overlay" />
          <span className="text-[10px] font-black text-white/50 uppercase tracking-[0.4em] mb-6 relative z-10">Neural Response</span>
          <p className="text-white text-xl font-black leading-relaxed tracking-tight relative z-10">{card.answer}</p>
        </div>
      </div>
    </div>
  );
};

export default SubjectView;
