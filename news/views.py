from django.shortcuts import render
from news.scripts.zeenews import zeenews
from news.scripts.indiatv import indiaTvscrape
from news.scripts.thehindu import hindu
from news.scripts.news18 import news18
from news.scripts.timesofindia import timesofindia
from news.scripts.indiatoday import indiatoday

from .models import NewsBox

from django.views.generic import CreateView
from django.urls import reverse_lazy
# Create your views here.

def home(request):
    scrape()
    return render(request, 'home.html', {})


def scrape():
    zeenews()
    indiaTvscrape()
    hindu()
    news18()
    timesofindia()
    indiatoday()

def get_news(request, src_name):
    news = NewsBox.objects.filter(src_name=src_name)
    return render(request, "news/news_by_src.html", {'news':news,'src_name':src_name})
    
