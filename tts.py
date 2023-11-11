import pyttsx3
from stt import text
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')
engine.setProperty('rate', 150)
engine.setProperty('pitch', 1.0)
engine.setProperty('volume', 1.0)
text = "Hello this is a student."
engine.say(text)
engine.runAndWait()