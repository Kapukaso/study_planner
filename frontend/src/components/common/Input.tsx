import React from 'react';
import { cn } from '../../lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, leftIcon, rightIcon, ...props }, ref) => {
    return (
      <div className="w-full space-y-2">
        {label && (
          <label className="block text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] ml-2">
            {label}
          </label>
        )}
        <div className="relative group">
          {leftIcon && (
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-cyan-400 transition-colors">
              {leftIcon}
            </div>
          )}
          <input
            ref={ref}
            className={cn(
              "w-full bg-white/5 border border-white/5 rounded-2xl px-6 py-4 text-white placeholder:text-slate-600 focus:outline-none focus:border-cyan-500/50 focus:bg-white/10 transition-all font-bold",
              leftIcon && "pl-12",
              rightIcon && "pr-12",
              error && "border-rose-500/50 focus:border-rose-500/50",
              className
            )}
            {...props}
          />
          {rightIcon && (
            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-cyan-400 transition-colors">
              {rightIcon}
            </div>
          )}
        </div>
        {error && (
          <p className="text-[10px] font-black text-rose-500 uppercase tracking-widest ml-2 animate-in fade-in slide-in-from-top-1">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
