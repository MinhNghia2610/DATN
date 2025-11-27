# aiva_core/tts.py
import pyttsx3

class TTSEngine:
    def __init__(self, cfg):
        self.engine = pyttsx3.init()
        rate = cfg.get('rate', 150)
        self.engine.setProperty('rate', rate)
        # voice selection omitted, depends on platform

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
