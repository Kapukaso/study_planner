import React from 'react';
import { Search, User } from 'lucide-react';

const Topbar: React.FC = () => {
  return (
    <header className="h-24 glass-morphism border-b border-white/5 px-12 flex items-center justify-between sticky top-0 z-40">
      <div className="relative w-[450px] group">
        <div className="absolute inset-0 bg-indigo-500/5 blur-xl group-focus-within:bg-indigo-500/10 transition-colors rounded-full" />
        <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
        <input 
          type="text" 
          placeholder="Quick search (Ctrl + K)" 
          className="relative w-full bg-slate-900/40 border border-white/10 rounded-2xl py-3 pl-14 pr-6 text-slate-200 focus:outline-none focus:ring-1 focus:ring-indigo-500/50 transition-all placeholder:text-slate-500 font-medium text-sm"
        />
        <div className="absolute right-4 top-1/2 -translate-y-1/2 flex gap-1">
          <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-white/10 text-[10px] font-black text-slate-500">CTRL</kbd>
          <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-white/10 text-[10px] font-black text-slate-500">K</kbd>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex flex-col items-end">
          <span className="text-xs font-black text-indigo-400 uppercase tracking-widest mb-0.5">Premium</span>
          <span className="text-sm font-bold text-slate-200">Alex Thompson</span>
        </div>
        <div className="relative group cursor-pointer">
          <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-violet-500 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
          <div className="relative w-12 h-12 rounded-2xl bg-slate-900 border border-white/10 flex items-center justify-center text-white overflow-hidden shadow-2xl">
            <img 
              src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex" 
              alt="Avatar"
              className="w-full h-full object-cover"
            />
          </div>
          <div className="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-500 border-2 border-slate-950 rounded-full" />
        </div>
      </div>
    </header>
  );
};

export default Topbar;
