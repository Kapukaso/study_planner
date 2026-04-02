import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, BarChart3, PlusCircle, BookOpen } from 'lucide-react';
import { cn } from '../../lib/utils';

interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  to: string;
}

const NavItem: React.FC<NavItemProps> = ({ icon, label, to }) => (
  <NavLink
    to={to}
    className={({ isActive }) => cn(
      "w-full flex items-center gap-3.5 px-6 py-4 rounded-2xl transition-all duration-500 font-bold group relative overflow-hidden text-left",
      isActive 
        ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-[0_0_20px_rgba(0,245,255,0.1)]" 
        : "text-slate-500 hover:bg-white/[0.03] hover:text-slate-200"
    )}
  >
    {({ isActive }) => (
      <>
        {isActive && (
          <span className="absolute left-0 w-1.5 h-6 bg-cyan-400 rounded-r-full shadow-[0_0_12px_rgba(0,245,255,0.6)]" />
        )}
        <span className={cn(
          "w-5 h-5 transition-transform duration-500 group-hover:scale-110",
          isActive ? "text-cyan-400" : "text-slate-600 group-hover:text-slate-300"
        )}>{icon}</span>
        <span className="text-xs tracking-[0.15em] uppercase font-black">{label}</span>
      </>
    )}
  </NavLink>
);

const Sidebar: React.FC = () => {
  return (
    <aside className="w-80 glass-morphism border-r border-white/5 flex flex-col p-8 relative z-50">
      <div className="mb-14 px-2 flex items-center gap-4">
        <NavLink to="/" className="flex items-center gap-4 group">
          <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl flex items-center justify-center shadow-[0_8px_24px_rgba(0,245,255,0.3)] overflow-hidden relative transition-transform group-hover:scale-105">
            <div className="absolute inset-0 bg-white/10 group-hover:bg-transparent transition-colors" />
            <BookOpen className="w-6 h-6 text-white relative z-10" />
          </div>
          <div>
            <h1 className="text-xl font-black text-white tracking-[-0.05em] leading-none">
              LEARNFLOW
            </h1>
            <p className="text-[10px] text-cyan-400/80 font-black uppercase tracking-[0.3em] mt-1.5">
              NEURAL STUDIO
            </p>
          </div>
        </NavLink>
      </div>

      <nav className="flex-1 space-y-4">
        <NavItem 
          icon={<LayoutDashboard className="w-5 h-5" />} 
          label="Neural Core" 
          to="/"
        />
        <NavItem 
          icon={<FileText className="w-5 h-5" />} 
          label="Knowledge base" 
          to="/knowledge"
        />
        <NavItem 
          icon={<BarChart3 className="w-5 h-5" />} 
          label="Deep Analytics" 
          to="/analytics"
        />
      </nav>

      <div className="mt-auto space-y-4">
        <div className="bg-cyan-500/[0.03] border border-cyan-500/10 rounded-3xl p-6 mb-4 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-20 h-20 bg-cyan-400/5 blur-2xl rounded-full -mr-10 -mt-10" />
          <p className="text-[10px] font-black text-cyan-400 uppercase tracking-widest mb-3">Upgrade</p>
          <p className="text-slate-400 text-xs font-bold leading-relaxed">Unlock Quantum Subject Analysis and 10GB Storage.</p>
        </div>

        <button 
          className="w-full bg-cyan-500 hover:bg-cyan-400 text-black p-5 rounded-2xl flex items-center justify-center gap-3 font-black text-xs uppercase tracking-[0.2em] shadow-[0_12px_40px_rgba(0,245,255,0.25)] hover:scale-[1.02] active:scale-[0.98] transition-all duration-300"
          onClick={() => {/* Open new subject modal */}}
        >
          <PlusCircle className="w-5 h-5" />
          <span>New Subject</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
