from django import template
from news.models import NewsBox
register = template.Library()


@register.inclusion_tag('news/news_list.html')
def zeenews_latest(count=5):
    news = NewsBox.objects.filter(src_name='Zee News')[:count]
    return {'news': news}

@register.inclusion_tag('news/news_list.html')
def indiatv_latest(count=5):
    news = NewsBox.objects.filter(src_name='IndiaTV')[:count]
    return {'news': news}

@register.inclusion_tag('news/news_list.html')
def hindu_latest(count=5):
    news = NewsBox.objects.filter(src_name='The Hindu')[:count]
    return {'news': news}

@register.inclusion_tag('news/without_img.html')
def news18(count=5):
    news = NewsBox.objects.filter(src_name='News18')[:count]
    return {'news': news}
    
@register.inclusion_tag('news/without_img.html')
def times_of_india(count=5):
    news = NewsBox.objects.filter(src_name='Times of India')[:count]
    return {'news': news}

@register.inclusion_tag('news/without_img.html')
def india_today(count=5):
    news = NewsBox.objects.filter(src_name='India Today')[:count]
    return {'news': news}