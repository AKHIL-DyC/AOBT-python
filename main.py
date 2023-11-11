from flask import Flask, render_template
from langchain.llms import OpenAI
import openai
import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import threading
#test
app = Flask(__name__)

@app.route("/")
def index():
    load_dotenv()

    api = os.getenv("API_KEY")
    print(api)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        speak="I am listening"
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        question=text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

    llm = OpenAI(openai_api_key=os.getenv("API_KEY"))

    answer = llm.predict(text)
    print(answer)

    
    threading.Thread(target=tts, args=(answer,)).start()

    
    return render_template('index.html',answer=answer,question=question,speak=speak)

def tts(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')
    engine.setProperty('rate', 150)
    engine.setProperty('pitch', 1.0)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    app.run(debug=True)
