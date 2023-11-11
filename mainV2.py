from langchain.llms import OpenAI
import openai
import os
from dotenv import main
from langchain.llms import openai
import speech_recognition as sr
import pyttsx3
from playsound import playsound

main.load_dotenv()
api = os.getenv("API_KEY")
print(api)


playsound("D:\\AOBT\\V2\\oSiri.mp3")


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

llm = OpenAI(openai_api_key=os.getenv("API_KEY"))
response = llm.predict(text)
print(response)


def tts(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')
    engine.setProperty('rate', 150)
    engine.setProperty('pitch', 1.0)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()


tts(response)
playsound("D:\\AOBT\\V2\\cSiri.mp3")
