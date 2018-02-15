import json

from django.test import TestCase
from django.shortcuts import resolve_url
from mixer.backend.django import mixer

from youtube_channel.my_videos.models import Theme, Thumb, Comment, Video


class PopularThemesView(TestCase):

    def setUp(self):
        mixer.cycle(20).blend(Theme)
        video = mixer.cycle(10).blend(Video)[0]

        self.principal_theme = mixer.blend(Theme, views=1000)
        video.themes.add(self.principal_theme)
        mixer.cycle(100).blend(Comment, is_positive=True, video=video)
        mixer.cycle(100).blend(Thumb, is_positive=True, video=video)

    def test_view(self):
        url = resolve_url('my_videos:popular_themes')
        response = self.client.get(url)
        self.assertEqual(10, len(json.loads(response.content)['themes']))

    def test_sort(self):
        url = resolve_url('my_videos:popular_themes')
        response = self.client.get(url)
        self.assertEqual(self.principal_theme.name, json.loads(response.content)['themes'][0])



