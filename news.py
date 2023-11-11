import requests
import os
from dotenv import load_dotenv
load_dotenv()

def news():
    newskey= os.getenv("news_key")
    main_url="https://newsapi.org/v2/top-headlines?country=in&apiKey="+newskey
    news=requests.get(main_url).json()
    article=news["articles"]

    news_article=[]
    for arti in article:
        news_article.append(arti['title'])

    for i in range(10):
        print(news_article[i])

news()
    