from django.test import TestCase
from django.db.utils import IntegrityError

from youtube_channel.my_videos.models import Theme

class TestThemeModel(TestCase):

    def test_create(self):
        self.assertEqual(0, Theme.objects.count())
        Theme.objects.create(name='Financial')
        self.assertEqual(1, Theme.objects.count())

    def test_uniqueness(self):
        Theme.objects.create(name='Machine Learning')
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name='Machine Learning')
