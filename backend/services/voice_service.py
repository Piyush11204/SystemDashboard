import speech_recognition as sr
import pyttsx3

class VoiceService:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def listen(self):
        """Listens to voice input and converts it to text."""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except Exception as e:
            raise Exception(f"Voice recognition error: {e}")

    def speak(self, text, voice_type='default'):
        """Converts text to speech."""
        self.engine.say(text)
        self.engine.runAndWait()
        return {"status": "success", "message": "Speech complete"}
