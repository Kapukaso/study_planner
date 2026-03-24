import React from 'react';
import { Brain } from 'lucide-react';
import { cn } from '../../lib/utils';

interface EmptyStateProps {
  title?: string;
  message: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
  className?: string;
}

const EmptyState: React.FC<EmptyStateProps> = ({ 
  title = "Empty Workspace", 
  message, 
  icon, 
  action,
  className 
}) => {
  return (
    <div className={cn(
      "glass-morphism-card border-white/5 rounded-[40px] p-12 md:p-20 text-center group border-2 border-dashed border-white/5 hover:border-indigo-500/20 transition-colors",
      className
    )}>
      <div className="w-20 h-20 md:w-24 md:h-24 bg-indigo-500/10 rounded-[32px] flex items-center justify-center mx-auto mb-8 group-hover:scale-110 transition-transform duration-500">
        {icon || <Brain className="w-10 h-10 md:w-12 md:h-12 text-indigo-400" />}
      </div>
      <h3 className="text-2xl md:text-3xl font-black text-white tracking-tight">{title}</h3>
      <p className="text-slate-500 mt-3 md:mt-4 max-w-sm mx-auto font-bold text-base md:text-lg leading-relaxed">
        {message}
      </p>
      {action && (
        <div className="mt-8 md:mt-10">
          {action}
        </div>
      )}
    </div>
  );
};

export default EmptyState;
