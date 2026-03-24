import React from 'react';
import { cn } from '../../lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'glass' | 'outline' | 'gradient';
  isHoverable?: boolean;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'glass', isHoverable = true, children, ...props }, ref) => {
    const variants = {
      glass: 'bg-slate-900/40 border border-white/5 backdrop-blur-xl',
      outline: 'bg-transparent border border-white/5 hover:border-white/10 transition-colors',
      gradient: 'bg-gradient-to-br from-slate-900/80 to-slate-950/80 border border-white/5 shadow-2xl shadow-indigo-500/10',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'rounded-[32px] p-6 transition-all duration-300',
          variants[variant],
          isHoverable && 'hover:border-indigo-500/30 hover:shadow-2xl hover:shadow-indigo-500/5',
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

export default Card;
