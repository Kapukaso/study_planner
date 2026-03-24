import React from 'react';
import { cn } from '../../lib/utils';

interface ProgressProps {
  value: number;
  max?: number;
  variant?: 'cyan' | 'purple' | 'indigo' | 'pink';
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  className?: string;
}

const Progress: React.FC<ProgressProps> = ({ 
  value, 
  max = 100, 
  variant = 'indigo', 
  size = 'md', 
  showLabel = false,
  className 
}) => {
  const percentage = Math.min(Math.max(0, (value / max) * 100), 100);

  const variants = {
    cyan: 'bg-cyan-500 shadow-[0_0_15px_rgba(6,182,212,0.5)]',
    purple: 'bg-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.5)]',
    indigo: 'bg-indigo-500 shadow-[0_0_15px_rgba(99,102,241,0.5)]',
    pink: 'bg-pink-500 shadow-[0_0_15px_rgba(236,72,153,0.5)]',
  };

  const sizes = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-4',
  };

  return (
    <div className={cn("w-full", className)}>
      {showLabel && (
        <div className="flex justify-between items-center mb-2">
          <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Progress</span>
          <span className="text-xs font-black text-white">{Math.round(percentage)}%</span>
        </div>
      )}
      <div className={cn("w-full bg-white/5 rounded-full overflow-hidden", sizes[size])}>
        <div 
          className={cn("h-full transition-all duration-1000 ease-out rounded-full", variants[variant])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default Progress;
