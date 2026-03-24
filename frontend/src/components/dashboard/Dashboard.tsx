import React from 'react';
import { Plus } from 'lucide-react';
import { useAppContext } from '../../context/AppContext';
import SubjectCard from './SubjectCard';
import Button from '../common/Button';
import EmptyState from '../common/EmptyState';

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
            Welcome back, Operator Thompson. Synthesis complete for <span className="text-cyan-400">{subjects.length} subjects</span>. 
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
        <EmptyState 
          title="Empty Workspace"
          message="Every master was once a beginner. Create your first subject to start your journey."
          action={
            <Button 
              variant="primary" 
              size="lg" 
              leftIcon={<Plus className="w-5 h-5" />}
              className="px-12"
            >
              Get Started
            </Button>
          }
        />
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
