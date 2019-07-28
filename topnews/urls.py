from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from news.views import home, get_news

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('news/<str:src_name>/', get_news, name="get_news"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
