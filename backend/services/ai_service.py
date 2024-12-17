import openai

class AIService:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        openai.api_key = api_key

    def chat_completion(self, messages):
        """Generates a response from OpenAI GPT model."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise Exception(f"AI chat error: {e}")
