# app/tts.py
import pyttsx3

def speak_text(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # adjust for clarity
    engine.say(text)
    engine.runAndWait()