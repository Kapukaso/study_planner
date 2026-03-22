import React from 'react';
import { BookOpen, FileText, CheckCircle2 } from 'lucide-react';
import type { Subject } from '../../types';
import { useAppContext } from '../../context/AppContext';

interface SubjectCardProps {
  subject: Subject;
}

const SubjectCard: React.FC<SubjectCardProps> = ({ subject }) => {
  const { setCurrentSubject } = useAppContext();

  return (
    <div 
      onClick={() => setCurrentSubject(subject)}
      className="group glass-morphism-card rounded-[32px] p-8 hover:bg-white/[0.04] transition-all duration-700 cursor-pointer relative overflow-hidden glow-card border border-white/[0.05] active:scale-[0.98]"
    >
      <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-400/[0.03] blur-3xl -mr-16 -mt-16 group-hover:bg-cyan-400/[0.08] transition-colors" />
      
      <div className="flex justify-between items-start mb-8 relative z-10">
        <div className="max-w-[80%]">
          <h3 className="text-2xl font-black text-white group-hover:text-cyan-400 transition-all duration-500 tracking-[-0.03em] leading-tight">
            {subject.name}
          </h3>
          <div className="flex items-center gap-2 mt-3">
            <span className="text-[9px] font-black uppercase tracking-[0.2em] text-cyan-400/60 bg-cyan-400/10 px-2 py-0.5 rounded-md border border-cyan-400/20">
              {subject.code || 'UNIT'}
            </span>
            <span className="w-1 h-1 rounded-full bg-slate-700" />
            <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Active Link</span>
          </div>
        </div>
        <div className="bg-white/5 text-slate-300 w-11 h-11 rounded-2xl flex items-center justify-center text-xs font-black border border-white/5 shadow-inner group-hover:bg-cyan-500 group-hover:text-black group-hover:border-cyan-400 transition-all duration-500">
          P{subject.priority}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6 pt-8 border-t border-white/[0.05] relative z-10">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-slate-600">
            <BookOpen className="w-3.5 h-3.5" />
            <span className="text-[8px] uppercase font-black tracking-[0.15em]">Modules</span>
          </div>
          <span className="block text-2xl font-black text-slate-100 group-hover:text-cyan-400 transition-colors duration-500">{subject.chapters_count}</span>
        </div>
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-slate-600">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span className="text-[8px] uppercase font-black tracking-[0.15em]">Topics</span>
          </div>
          <span className="block text-2xl font-black text-slate-100 group-hover:text-purple-400 transition-colors duration-500">{subject.topics_count}</span>
        </div>
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-slate-600">
            <FileText className="w-3.5 h-3.5" />
            <span className="text-[8px] uppercase font-black tracking-[0.15em]">Assets</span>
          </div>
          <span className="block text-2xl font-black text-slate-100 group-hover:text-blue-400 transition-colors duration-500">{subject.documents_count}</span>
        </div>
      </div>
      
      <div className="mt-8 relative z-10">
        <div className="h-[3px] w-full bg-slate-900 rounded-full overflow-hidden">
          <div 
            className="h-full bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 rounded-full group-hover:shadow-[0_0_12px_rgba(0,245,255,0.6)] transition-all duration-1000 ease-out" 
            style={{ width: '45%' }}
          />
        </div>
        <div className="flex justify-between mt-3">
          <span className="text-[9px] font-black text-slate-600 uppercase tracking-widest">Efficiency Sync</span>
          <span className="text-[9px] font-black text-cyan-400 tracking-widest">45%</span>
        </div>
      </div>
    </div>
  );
};

export default SubjectCard;
