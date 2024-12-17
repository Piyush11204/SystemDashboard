import  { useState } from 'react';
import axios from 'axios';

const VoiceControl = () => {
  const [listeningText, setListeningText] = useState('');
  const [speaking, setSpeaking] = useState(false);

  const handleListen = async () => {
    try {
      const result = await axios.get('http://localhost:5000/listen');
      setListeningText(result.data.text || 'No text detected');
    } catch (error) {
      console.error('Listening error:', error);
    }
  };

  const handleSpeak = async () => {
    if (!listeningText) return;
    setSpeaking(true);
    try {
      await axios.post('http://localhost:5000/speak', { 
        text: listeningText, 
        voice_type: 'default' 
      });
    } catch (error) {
      console.error('Speaking error:', error);
    } finally {
      setSpeaking(false);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h1 className="text-2xl font-bold mb-4">Voice Control</h1>
      <div className="space-y-4">
        <button
          onClick={handleListen}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors"
        >
          Listen
        </button>
        <button
          onClick={handleSpeak}
          disabled={speaking || !listeningText}
          className="bg-blue-500 text-white px-4 py-2 rounded ml-4 hover:bg-blue-600 transition-colors"
        >
          {speaking ? 'Speaking...' : 'Speak'}
        </button>
        {listeningText && (
          <div className="bg-gray-100 p-4 rounded-md mt-4">
            <p>{listeningText}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default VoiceControl;