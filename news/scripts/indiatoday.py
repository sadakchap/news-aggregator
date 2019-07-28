from bs4 import BeautifulSoup
import requests
from news.models import NewsBox

requests.packages.urllib3.disable_warnings()

url = 'https://www.indiatoday.in/'
source = requests.get(url).text

soup = BeautifulSoup(source, "lxml")

news_box = soup.find('ul', class_='itg-listing')
# print(news_box.prettify())

def indiatoday():
    for news_story in news_box.find_all('li')[:7]:
        news_link = url + news_story.find('a').get('href')
        img_src = None
        news_title = news_story.find('a').text

        if not NewsBox.objects.filter(news_link=news_link).exists():
            news = NewsBox()
            news.src_name = 'India Today'
            news.src_link = url
            news.title = news_title
            news.news_link = news_link
            news.img = img_src
            news.save()


    # print(news_link)
    # print(news_title)
    # print('*'*80)
