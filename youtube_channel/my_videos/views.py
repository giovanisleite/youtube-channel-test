from django.shortcuts import render
from django.http import JsonResponse

from youtube_channel.my_videos.models import Theme

def popular_themes(request):
    if request.method == 'GET':
        themes = [theme.name for theme in sorted(Theme.objects.all(), key=lambda t: t.success)[:-10:-1]]
    return JsonResponse({'themes': themes})
