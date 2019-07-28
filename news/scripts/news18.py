from bs4 import BeautifulSoup
import requests
from news.models import NewsBox

requests.packages.urllib3.disable_warnings()

url ='https://www.news18.com/'
source = requests.get(url).text

soup = BeautifulSoup(source, "lxml")

news_box = soup.find('ul', class_='lead-mstory')

def news18():
    for news_story in news_box.find_all('li')[:7]:
        news_link = news_story.find('a')
        img_src = None
        news_title = news_link.text

        news_link = news_link.get('href')

        if NewsBox.objects.filter(news_link=news_link).exists():
            pass
        else:
            news = NewsBox()
            news.src_name = 'News18'
            news.src_link = url
            news.title = news_title
            news.news_link = news_link
            news.img = img_src
            news.save()




