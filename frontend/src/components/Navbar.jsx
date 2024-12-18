import { Link } from 'react-router-dom';
import { 
  Home, 
  Mic, 
  Monitor, 
  MessageCircle 
} from 'lucide-react';


const Navbar = () => {
  return (
    <div className="w-64 bg-gray-800 text-white p-4">
      <div className="mb-10">
        <h1 className="text-2xl font-bold text-center">Jarvis AI</h1>
      </div>
      <nav>
        <ul className="space-y-2">
          {[
            { path: '/', icon: Home, label: 'Dashboard' },
            { path: '/voice', icon: Mic, label: 'Voice Control' },
            { path: '/system', icon: Monitor, label: 'System Control' },
            { path: '/chat', icon: MessageCircle, label: 'AI Chat' }
          ].map(({ path, icon: Icon, label }) => (
            <li key={path}>
              <Link 
                to={path} 
                className="flex items-center p-3 hover:bg-gray-700 rounded transition-colors"
              >
                <Icon className="w-6 h-6 mr-3" />
                {label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Navbar;
