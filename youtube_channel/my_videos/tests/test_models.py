from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils import timezone

from youtube_channel.my_videos.models import Theme, Video, Comment, Thumb


class TestTheme(TestCase):

    def setUp(self):
        self.theme = Theme.objects.create(name='Machine Learning')

    def test_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name='Machine Learning')

    def test_success(self):
        fake_data = {'date_uploaded': timezone.now(),
                     'views': 10}

        videos = [Video.objects.create(title='Machine Learning', **fake_data),
                  Video.objects.create(title='NLP', **fake_data)]

        for video in videos:
            video.themes.add(self.theme)
            fake_interaction = {'time': timezone.now(), 'video': video}
            Comment.objects.create(is_positive=True, **fake_interaction)
            Comment.objects.create(is_positive=False, **fake_interaction)
            Thumb.objects.create(is_positive=True, **fake_interaction)
            Thumb.objects.create(is_positive=False, **fake_interaction)

        self.assertEqual(10, self.theme.success())


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

    def test_score(self):
        fake_interaction = {'time': timezone.now(), 'video': self.video}
        Comment.objects.create(is_positive=True, **fake_interaction)
        Comment.objects.create(is_positive=False, **fake_interaction)
        Thumb.objects.create(is_positive=True, **fake_interaction)
        Thumb.objects.create(is_positive=False, **fake_interaction)

        self.assertEqual(5, self.video.score)

