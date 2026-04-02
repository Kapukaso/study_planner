import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, User, UserPlus, BookOpen } from 'lucide-react';
import api from '../../services/api';
import Input from '../common/Input';
import Button from '../common/Button';

const RegisterPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await api.post('/api/auth/register', {
        email,
        username,
        password,
        full_name: fullName,
      });

      // Redirect to login after successful registration
      navigate('/login');
    } catch (err: any) {
      console.error('Registration failed:', err);
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#020205] text-[#f5f5f7] flex items-center justify-center p-6 relative overflow-hidden">
      {/* Precision background lights */}
      <div className="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-cyan-500/10 blur-[160px] rounded-full pointer-events-none" />
      <div className="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/10 blur-[160px] rounded-full pointer-events-none" />
      
      <div className="w-full max-w-md relative z-10">
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-2xl mb-6 shadow-[0_8px_32px_rgba(0,245,255,0.4)] relative group overflow-hidden">
            <div className="absolute inset-0 bg-white/10 group-hover:bg-transparent transition-colors" />
            <BookOpen className="w-8 h-8 text-white relative z-10" />
          </div>
          <h1 className="text-4xl font-black tracking-tight mb-2">JOIN FLOW</h1>
          <p className="text-cyan-400 font-black uppercase tracking-[0.3em] text-xs">Register Neural Core</p>
        </div>

        <div className="glass-morphism border border-white/5 p-8 rounded-[32px] shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-cyan-500/5 blur-3xl rounded-full -mr-16 -mt-16" />
          
          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label="Full Neural Name"
              placeholder="e.g. John Doe"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              leftIcon={<User className="w-5 h-5" />}
            />

            <Input
              label="Neural ID (Username)"
              placeholder="Pick a unique ID"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              leftIcon={<UserPlus className="w-5 h-5" />}
              required
            />

            <Input
              label="Sync Email"
              type="email"
              placeholder="your@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              leftIcon={<Mail className="w-5 h-5" />}
              required
            />
            
            <Input
              label="Security Key (Password)"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              leftIcon={<Lock className="w-5 h-5" />}
              required
            />

            {error && (
              <div className="bg-rose-500/10 border border-rose-500/20 p-4 rounded-2xl text-rose-500 text-xs font-black uppercase tracking-widest text-center">
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full py-5 rounded-2xl bg-cyan-500 hover:bg-cyan-400 text-black font-black uppercase tracking-[0.2em] shadow-[0_12px_40px_rgba(0,245,255,0.25)] transition-all active:scale-[0.98]"
              isLoading={isLoading}
              rightIcon={<UserPlus className="w-5 h-5" />}
            >
              Initialize Sync
            </Button>
          </form>

          <div className="mt-8 pt-8 border-t border-white/5 text-center">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">
              Already Synced?{' '}
              <Link to="/login" className="text-cyan-400 hover:text-cyan-300 transition-colors">
                Initiate Login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
