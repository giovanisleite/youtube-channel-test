from django.urls import path

from youtube_channel.my_videos.views import popular_themes

app_name = 'my_videos'

urlpatterns = [
    path('get_popular_themes/', popular_themes, name='popular_themes')
]
