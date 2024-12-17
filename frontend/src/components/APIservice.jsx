const BASE_URL = 'http://localhost:5000';

const apiService = {
  listenVoice: async () => {
    try {
      const response = await fetch(`${BASE_URL}/listen`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });

      if (!response.ok) throw new Error('Voice listening failed');

      return await response.json();
    } catch (error) {
      console.error('Voice listening error', error);
      throw error;
    }
  },

  aiChat: async (prompt) => {
    try {
      const response = await fetch(`${BASE_URL}/ai-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) throw new Error('AI Chat request failed');

      return await response.json();
    } catch (error) {
      console.error('AI Chat error', error);
      throw error;
    }
  },

  systemControl: async (command) => {
    try {
      const response = await fetch(`${BASE_URL}/system-control`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command }),
      });

      if (!response.ok) throw new Error('System control request failed');

      return await response.json();
    } catch (error) {
      console.error('System Control error', error);
      throw error;
    }
  },

  speak: async (text, voiceType = 'primary') => {
    try {
      const response = await fetch(`${BASE_URL}/speak`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, voice_type: voiceType }),
      });

      if (!response.ok) throw new Error('Speaking request failed');

      return await response.json();
    } catch (error) {
      console.error('Speaking error', error);
      throw error;
    }
  },
};

export default apiService;
