from bs4 import BeautifulSoup
import requests
from news.models import NewsBox
import os
import shutil
from django.conf import settings

session = requests.Session()
session.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36'}

requests.packages.urllib3.disable_warnings()

url = 'https://zeenews.india.com'

source = requests.get(url).text

soup = BeautifulSoup(source, "lxml")

def zeenews():
    for news_story in soup.find_all('div', class_='mini-list-story')[:7]:
        news_link = news_story.find('div', class_='m-img-block').a
        img_src = news_link.find('img').get('src')
        news_card = news_story.find('div', class_='mini-con')
        news_title = news_card.find('h3').a.text

        news_link = url + news_link.get('href')
        if not NewsBox.objects.filter(news_link=news_link).exists():
            news = NewsBox()
            news.src_name = 'Zee News'
            news.src_link = url
            news.title = news_title
            news.news_link = news_link

            body = b''
            # start of stackoverflow
            media_root = settings.MEDIA_ROOT
            if not img_src.startswith(("data:image", "javascript")):
                local_filename = img_src.split('/')[-1].split("?")[0]
                r = session.get(img_src, stream=True, verify=False)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)
                        body += chunk

                # current_image_absolute_path = os.path.abspath(local_filename)
                # shutil.move(current_image_absolute_path, media_root)
            # end of stackoverflow
            news.img = local_filename
            news.save()

            import boto3
            s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
            bucket.put_object(Key=f'media/{news.img.name}', Body=body)

