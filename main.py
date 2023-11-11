from flask import Flask,session, request, render_template
from flask_session import Session
from langchain.llms import OpenAI
import openai
import os
import time
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)
app.config["SESSION_TYPE"]="filesystem"

Session(app)
def slow_loading_function():
    """Simulates a time consuming process (wait 10 seconds and return a reversed string)"""
    time.sleep(1)
@app.route("/")
def home():
    return render_template('index.html')
@app.route("/loading", methods=["POST"])
def loading():
    if request.method == "POST":
        # We'll use a session object to save the data sent by the user for processing
        #session["user_data"] = request.form.get("user_data")
        return render_template("loading.html")
    
@app.route("/ai")
def ai():
    # Finally, use the user data in some intensive process
    slow_loading_function()

    api = os.getenv("API_KEY")
    print(api)

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak something...")
        speak = "I am listening"
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        question = text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

    llm = OpenAI(openai_api_key=os.getenv("API_KEY"))

    answer = llm.predict(text)
    print(answer)

    threading.Thread(target=tts, args=(answer,)).start()

    return render_template('ai.html', answer=answer, question=question, speak=speak)

def tts(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')
    engine.setProperty('rate', 150)
    engine.setProperty('pitch', 1.0)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

#@app.route()
if __name__ == "__main__":
    app.run(debug=True)

