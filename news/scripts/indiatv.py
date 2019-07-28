from bs4 import BeautifulSoup
import requests
from news.models import NewsBox
import os
import shutil
from django.conf import settings

session = requests.Session()
session.headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36'}

url = 'https://www.indiatvnews.com/'
source = requests.get(url).text

soup = BeautifulSoup(source, "lxml")

news_box=soup.find('ul', class_=['normal'])

requests.packages.urllib3.disable_warnings()

def indiaTvscrape():
    for news_story in news_box.find_all('li')[:7]:
        news_link = news_story.find('a')
        img_src = news_link.find('img').get('data-original')
        news_card = news_story.find('div',class_='text_box')
        news_title = news_card.find('h2', class_='title').a.text

        news_link = news_link.get('href')

        if not NewsBox.objects.filter(news_link=news_link).exists():
            news = NewsBox()
            news.src_name = 'IndiaTV'
            news.src_link = url
            news.title = news_title
            news.news_link = news_link
            
            # stackoverflow solution
            # img_src = obj['news_img_src']
            
            body = b''

            media_root = settings.MEDIA_ROOT
            if not img_src.startswith(("data:image", "javascript")):
                local_filename = img_src.split('/')[-1].split("?")[0]
                r = session.get(img_src, stream=True, verify=False)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        f.write(chunk)
                        body += chunk

                # current_image_absolute_path = os.path.abspath(local_filename)
                # try:
                #     shutil.move(current_image_absolute_path, media_root)
                # except:
                #     pass

            # end of stackoverflow
            news.img = local_filename
            news.save()
            
            import boto3
            s3 = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
            bucket.put_object(Key=f'media/{news.img.name}', Body=body)