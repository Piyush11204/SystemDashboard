import  { useState } from 'react';
import { Mic,  Send } from 'lucide-react';
import apiService from './APIservice.jsx';
// import voiceService from './services/voiceService';

const JarvisAssistant = () => {
  const [listening, setListening] = useState(false);
  const [voiceCommand, setVoiceCommand] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  // const [systemStatus, setSystemStatus] = useState('');

  const startListening = async () => {
    setListening(true);
    try {
      const result = await apiService.listenVoice();
      setVoiceCommand(result.text);
      
      // Trigger AI processing
      const aiResult = await apiService.aiChat(result.text);
      setAiResponse(aiResult.response);

      // Optional system control
      await apiService.systemControl(result.text);
    } catch (error) {
      console.error('Error processing voice command', error);
    } finally {
      setListening(false);
    }
  };

  const handleSendCommand = async () => {
    if (voiceCommand) {
      const aiResult = await apiService.aiChat(voiceCommand);
      setAiResponse(aiResult.response);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <div className="container mx-auto p-6">
        <h1 className="text-4xl font-bold mb-6 text-center">
          JARVIS Assistant
        </h1>

        <div className="bg-gray-800 rounded-lg p-6 mb-6">
          <div className="flex items-center space-x-4 mb-4">
            <input
              type="text"
              value={voiceCommand}
              onChange={(e) => setVoiceCommand(e.target.value)}
              placeholder="Voice Command or Text Input"
              className="flex-grow p-2 bg-gray-700 rounded"
            />
            <button 
              onClick={startListening} 
              className={`p-2 rounded ${listening ? 'bg-red-600' : 'bg-blue-600'}`}
            >
              <Mic className="w-6 h-6" />
            </button>
            <button onClick={handleSendCommand} className="p-2 bg-green-600 rounded">
              <Send className="w-6 h-6" />
            </button>
          </div>

          <div className="mt-4">
            <h3 className="text-xl font-semibold mb-2">AI Response:</h3>
            <div className="bg-gray-700 p-4 rounded">
              {aiResponse || 'Waiting for command...'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JarvisAssistant;