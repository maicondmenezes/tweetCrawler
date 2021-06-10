from django.urls import path

from . import views

app_name = 'tweet_crawl'

urlpatterns = [
    path('', views.index, name='index'),
    path('querie_list/', views.querie_list, name='querie_list'),
    path('querie/<int:querie_id>/', views.tweet_list, name='tweet_list'),
    path('querie/<int:querie_id>/analisys/', views.analisys, name='analisys'),
    path('tweet/<int:tweet_id>', views.tweet, name='tweet'),
    path('search', views.search, name='search'),
]