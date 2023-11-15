from flask import Flask, session, request, render_template,url_for
from flask_session import Session
from langchain.llms import OpenAI
import openai
import os
import time
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import threading
import keyboard
import requests
import pythoncom

flag = 0
app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

def ttse(text):
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')
    engine.setProperty('rate', 150)
    engine.setProperty('pitch', 1.0)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()
pythoncom.CoUninitialize()   
def slow_loading_function():
    """Simulates a time-consuming process (wait 10 seconds and return a reversed string)"""
    time.sleep(1)


@app.route("/")

def home():
    font_url = url_for('static', filename='fonts/nothing.ttf')
    return render_template('index.html',nothing=font_url)


@app.route("/loading", methods=["POST"])
def loading():
    if request.method == "POST":
        
    
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


@app.route("/news")
def news_route():
    global flag
    if request.method == "GET":
        newskey = os.getenv("news_key")

        if newskey is None:
            print("API key 'news_key' not found in your .env file.")
            return

        main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + newskey
        news_data = requests.get(main_url).json()
        articles = news_data.get("articles", [])

        news_article = [arti.get('title', '') for arti in articles]

        print("News started. Press 'Spacebar' to end.")

        nws = ""  # Initialize nws variable

        for i in range(10):
            if flag == 1:
                break
            nws += news_article[i] + "   "
            print(news_article[i])
            text = news_article[i]
            threading.Thread(target=ttse, args=(nws,)).start()

        return render_template('news.html', news=nws)
if __name__ == "__main__":
    app.run()