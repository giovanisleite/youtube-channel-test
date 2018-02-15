from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils import timezone

from youtube_channel.my_videos.models import Theme, Video


class TestTheme(TestCase):

    def test_uniqueness(self):
        Theme.objects.create(name='Machine Learning')
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name='Machine Learning')


class TestVideo(TestCase):

    def setUp(self):
        self.fake_data = {'title': 'Machine Learning 101',
                          'date_uploaded': timezone.now(),
                          'views': 10}
        self.video = Video.objects.create(**self.fake_data)
        self.theme = Theme.objects.create(name='Machine Learning')

    def test_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Video.objects.create(**self.fake_data)

    def test_themes_relation(self):
        self.assertEqual(0, self.video.themes.count())
        self.video.themes.add(self.theme)
        self.assertEqual(1, self.video.themes.count())
