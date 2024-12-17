
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard.jsx';
import VoiceControl from './pages/VoiceControl';
import SystemControl from './pages/SystemControl.jsx';
import AIChat from './pages/AIChat';

const App = () => {
  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <Navbar />
        <div className="flex-grow p-6 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/voice" element={<VoiceControl />} />
            <Route path="/system" element={<SystemControl />} />
            <Route path="/chat" element={<AIChat />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;