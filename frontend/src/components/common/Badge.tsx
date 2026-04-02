import React from 'react';
import { cn } from '../../lib/utils';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'cyan' | 'purple' | 'pink' | 'success' | 'danger' | 'outline';
  size?: 'xs' | 'sm';
}

const Badge: React.FC<BadgeProps> = ({ className, variant = 'primary', size = 'sm', children, ...props }) => {
  const variants = {
    primary: 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20',
    cyan: 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    pink: 'bg-pink-500/10 text-pink-400 border-pink-500/20',
    success: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    danger: 'bg-rose-500/10 text-rose-400 border-rose-500/20',
    outline: 'bg-transparent text-slate-500 border-slate-800',
  };

  const sizes = {
    xs: 'px-2 py-0.5 text-[8px]',
    sm: 'px-3 py-1 text-[10px]',
  };

  return (
    <span
      className={cn(
        'rounded-full font-black uppercase tracking-widest border',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};

export default Badge;
