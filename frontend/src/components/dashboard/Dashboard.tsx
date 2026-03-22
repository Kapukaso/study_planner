import React from 'react';
import { Plus } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import SubjectCard from './SubjectCard';

const Dashboard: React.FC = () => {
  const { subjects, loading } = useAppContext();

  return (
    <div className="animate-in fade-in slide-in-from-bottom-8 duration-1000 max-w-7xl mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-16 gap-8 relative">
        <div className="absolute top-0 right-0 w-80 h-80 bg-cyan-500/5 blur-[120px] -z-10 animate-pulse" />
        <div>
          <h2 className="text-6xl font-black text-white tracking-[-0.04em] mb-4 leading-[0.9]">
            Neural <span className="text-cyan-400 italic">Interface</span>
          </h2>
          <p className="text-slate-500 font-bold text-lg max-w-lg leading-relaxed border-l-2 border-cyan-500/20 pl-6 mt-6">
            Welcome back, Operator Thompson. Synthesis complete for <span className="text-cyan-400">7 subjects</span>. 
          </p>
        </div>
        <div className="flex gap-6">
          <div className="glass-morphism-card px-8 py-5 rounded-[28px] border border-white/5 group hover:border-cyan-500/30 transition-colors">
            <span className="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-2">Sync Time</span>
            <span className="text-3xl font-black text-white group-hover:text-cyan-400 transition-colors">24.5h</span>
          </div>
          <div className="glass-morphism-card px-8 py-5 rounded-[28px] border border-white/5 group hover:border-purple-500/30 transition-colors">
            <span className="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] mb-2">Efficiency</span>
            <span className="text-3xl font-black text-white group-hover:text-purple-400 transition-colors">82%</span>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-[340px] glass-morphism-card rounded-[32px] animate-pulse" />
          ))}
        </div>
      ) : subjects.length === 0 ? (
        <div className="glass-morphism-card border-white/5 rounded-[40px] p-12 md:p-20 text-center group border-2 border-dashed border-white/5 hover:border-indigo-500/20 transition-colors">
          <div className="w-20 h-20 md:w-24 md:h-24 bg-indigo-500/10 rounded-[32px] flex items-center justify-center mx-auto mb-8 group-hover:scale-110 transition-transform duration-500">
            <Plus className="w-10 h-10 md:w-12 md:h-12 text-indigo-400 group-hover:rotate-90 transition-transform duration-500" />
          </div>
          <h3 className="text-2xl md:text-3xl font-black text-white tracking-tight">Empty Workspace</h3>
          <p className="text-slate-500 mt-3 md:mt-4 max-w-sm mx-auto font-bold text-base md:text-lg leading-relaxed">
            Every master was once a beginner. Create your first subject to start your journey.
          </p>
          <button className="mt-8 md:mt-10 bg-white text-slate-950 px-8 md:px-10 py-3 md:py-4 rounded-2xl font-black uppercase tracking-wider text-xs md:text-sm hover:bg-indigo-500 hover:text-white transition-all shadow-xl shadow-white/5">
            Get Started
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {subjects.map(subject => (
            <SubjectCard key={subject.id} subject={subject} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
