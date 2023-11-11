import requests
import os
from dotenv import load_dotenv
import pyttsx3
import keyboard

load_dotenv()

flag = 0


def on_key_event(e):
    global flag
    if e.name == 'space':
        print("Spacebar pressed. News Ended.")
        flag = 1


keyboard.on_press(on_key_event)


def news():
    global flag

    newskey = os.getenv("news_key")

    if newskey is None:
        print("API key 'news_key' not found in your .env file.")
        return

    main_url = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + newskey
    news = requests.get(main_url).json()
    article = news["articles"]

    news_article = []
    for arti in article:
        news_article.append(arti['title'])
    print("News started. Press 'Spacebar' to end.")

    for i in range(10):
        if flag == 1:
            break
        print(news_article[i])
        engine = pyttsx3.init(driverName='sapi5')
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.karen')
        engine.setProperty('rate', 150)
        engine.setProperty('pitch', 1.0)
        engine.setProperty('volume', 1.0)
        text = news_article[i]
        engine.say(text)
        engine.runAndWait()


news()
