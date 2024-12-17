import { Sparkles, Server, Volume2 } from 'lucide-react';

const Dashboard = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {[
        {
          icon: Sparkles,
          title: 'AI Capabilities',
          description: 'Advanced natural language processing',
          color: 'text-blue-500'
        },
        {
          icon: Server,
          title: 'System Control',
          description: 'Manage computer functions seamlessly',
          color: 'text-green-500'
        },
        {
          icon: Volume2,
          title: 'Voice Interaction',
          description: 'Speech-to-text and text-to-speech',
          color: 'text-purple-500'
        }
      ].map(({ icon: Icon, title, description, color }) => (
        <div 
          key={title} 
          className="bg-white shadow-md rounded-lg p-6 hover:shadow-xl transition-shadow"
        >
          <Icon className={`w-12 h-12 mb-4 ${color}`} />
          <h2 className="text-xl font-semibold mb-2">{title}</h2>
          <p className="text-gray-600">{description}</p>
        </div>
      ))}
    </div>
  );
};

export default Dashboard;
