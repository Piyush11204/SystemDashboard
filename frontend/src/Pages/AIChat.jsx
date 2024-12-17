import  { useState } from 'react';
import axios from 'axios';

const AIChat = () => {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChat = async () => {
    setLoading(true);
    try {
      const result = await axios.post('http://localhost:5000/ai-chat', { prompt });
      setResponse(result.data.response);
    } catch (error) {
      console.error('Chat error:', error);
      setResponse('Sorry, something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h1 className="text-2xl font-bold mb-4">AI Chat</h1>
      <div className="flex mb-4">
        <input 
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ask me anything..."
          className="flex-grow p-2 border rounded-l-md"
        />
        <button 
          onClick={handleChat}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600 transition-colors"
        >
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </div>
      {response && (
        <div className="bg-gray-100 p-4 rounded-md mt-4">
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};

export default AIChat;