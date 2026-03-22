import Sidebar from './components/layout/Sidebar';
import Topbar from './components/layout/Topbar';
import Dashboard from './components/dashboard/Dashboard';
import SubjectView from './components/subject/SubjectView';
import { useAppContext } from './context/AppContext';

function App() {
  const { currentSubject } = useAppContext();

  return (
    <div className="flex h-screen bg-[#020205] text-[#f5f5f7] font-sans selection:bg-cyan-500/30 noise-overlay">
      {/* Precision background lights */}
      <div className="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] bg-cyan-500/5 blur-[160px] rounded-full pointer-events-none" />
      <div className="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-600/5 blur-[160px] rounded-full pointer-events-none" />
      <div className="fixed top-[30%] left-[40%] w-[20%] h-[20%] bg-blue-500/5 blur-[120px] rounded-full pointer-events-none animate-pulse" />

      <Sidebar />
      
      <main className="flex-1 flex flex-col overflow-hidden relative z-10">
        <Topbar />
        
        <div className="flex-1 overflow-y-auto p-10 custom-scrollbar">
          {currentSubject ? (
            <SubjectView />
          ) : (
            <Dashboard />
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
