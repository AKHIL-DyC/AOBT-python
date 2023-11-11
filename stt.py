import speech_recognition as sr
import pyttsx3
def tts(text):
      engine = pyttsx3.init(driverName='sapi5')
      engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')
      engine.setProperty('rate', 150)
      engine.setProperty('pitch', 1.0)
      engine.setProperty('volume', 1.0)
      engine.say(text)
      engine.runAndWait()
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak something...")
    recognizer.adjust_for_ambient_noise(source)  
    audio = recognizer.listen(source, timeout=5)
try:
    text = recognizer.recognize_google(audio)
    print("You said: " + text)
except sr.UnknownValueError:
    print("Sorry, I could not understand what you said.")
except sr.RequestError as e:
    print(f"Could not request results; {e}")
tts(text)