import React, { useState } from 'react';
import { Search, LogOut, Settings, User as UserIcon, Shield } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const Topbar: React.FC = () => {
  const { user, logout } = useAuth();
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  return (
    <header className="h-28 glass-morphism border-b border-white/5 px-12 flex items-center justify-between sticky top-0 z-40 bg-[#020205]/40 backdrop-blur-3xl">
      <div className="relative w-[500px] group">
        <div className="absolute inset-0 bg-cyan-500/5 blur-2xl group-focus-within:bg-cyan-500/10 transition-colors rounded-full" />
        <Search className="absolute left-6 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-cyan-400 transition-colors" />
        <input 
          type="text" 
          placeholder="Neural Search (Ctrl + K)" 
          className="relative w-full bg-white/[0.03] border border-white/10 rounded-[20px] py-4 pl-16 pr-8 text-slate-200 focus:outline-none focus:border-cyan-500/50 transition-all placeholder:text-slate-600 font-bold text-xs uppercase tracking-widest"
        />
        <div className="absolute right-6 top-1/2 -translate-y-1/2 flex gap-1.5 pointer-events-none opacity-40">
          <kbd className="px-2 py-1 rounded-lg bg-white/5 border border-white/10 text-[9px] font-black text-slate-400 tracking-tighter">CTRL</kbd>
          <kbd className="px-2 py-1 rounded-lg bg-white/5 border border-white/10 text-[9px] font-black text-slate-400 tracking-tighter">K</kbd>
        </div>
      </div>

      <div className="flex items-center gap-10">
        <div className="hidden xl:flex flex-col items-end">
          <div className="flex items-center gap-2 mb-1.5">
            <Shield className="w-3.5 h-3.5 text-cyan-400" />
            <span className="text-[10px] font-black text-cyan-400 uppercase tracking-[0.3em]">Quantum Link</span>
          </div>
          <span className="text-sm font-black text-white tracking-tight">{user?.full_name || user?.username || 'Operator'}</span>
        </div>

        <div className="relative">
          <div 
            className="group relative cursor-pointer"
            onClick={() => setShowProfileMenu(!showProfileMenu)}
          >
            <div className="absolute -inset-1.5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-[22px] blur opacity-20 group-hover:opacity-40 transition duration-700" />
            <div className="relative w-14 h-14 rounded-[20px] bg-slate-900 border border-white/10 flex items-center justify-center text-white overflow-hidden shadow-2xl transition-transform active:scale-95">
              <img 
                src={`https://api.dicebear.com/7.x/bottts-neutral/svg?seed=${user?.username || 'Guest'}`} 
                alt="Avatar"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-cyan-500 border-[3px] border-[#020205] rounded-full shadow-[0_0_10px_rgba(0,245,255,0.5)]" />
          </div>

          {/* Profile Dropdown */}
          {showProfileMenu && (
            <>
              <div 
                className="fixed inset-0 z-10" 
                onClick={() => setShowProfileMenu(false)}
              />
              <div className="absolute right-0 mt-6 w-72 glass-morphism border border-white/5 rounded-[32px] p-4 shadow-2xl z-20 animate-in fade-in zoom-in-95 duration-300">
                <div className="p-4 border-b border-white/5 mb-2">
                  <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1">Authenticated as</p>
                  <p className="text-white font-black truncate">{user?.email}</p>
                </div>
                
                <div className="space-y-1">
                  <button className="w-full flex items-center gap-4 px-4 py-4 text-slate-400 hover:text-white hover:bg-white/5 rounded-2xl transition-all font-bold text-xs uppercase tracking-widest group">
                    <UserIcon className="w-4 h-4 text-slate-500 group-hover:text-cyan-400" />
                    Neural Profile
                  </button>
                  <button className="w-full flex items-center gap-4 px-4 py-4 text-slate-400 hover:text-white hover:bg-white/5 rounded-2xl transition-all font-bold text-xs uppercase tracking-widest group">
                    <Settings className="w-4 h-4 text-slate-500 group-hover:text-cyan-400" />
                    System Core
                  </button>
                  <div className="h-px bg-white/5 my-2 mx-4" />
                  <button 
                    onClick={() => logout()}
                    className="w-full flex items-center gap-4 px-4 py-4 text-rose-500 hover:bg-rose-500/10 rounded-2xl transition-all font-bold text-xs uppercase tracking-widest group"
                  >
                    <LogOut className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                    Terminate Sync
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Topbar;
