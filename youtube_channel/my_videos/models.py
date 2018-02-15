from django.db import models
from django.utils import timezone

from datetime import timedelta

class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)

    @property
    def success(self):
        a_year_ago = timezone.now() - timedelta(days=365)
        return sum([video.score for video in self.videos.filter(date_uploaded__gte=a_year_ago)])

    def srt(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=50, unique=True)
    date_uploaded = models.DateTimeField(blank=True)
    views = models.IntegerField(default=0)
    themes = models.ManyToManyField(Theme, related_name='videos')

    @property
    def score(self):
        days_since_upload = (timezone.now() - self.date_uploaded).days
        time_factor = max(0, 1 - days_since_upload/365)

        all_comments = self.comments.count()
        good_comments = self.comments.filter(is_positive=True).count()/all_comments if all_comments > 0 else 0

        all_thumbs = self.thumbs.count()
        thumbs_up = self.thumbs.filter(is_positive=True).count()/all_thumbs if all_thumbs > 0 else 0

        positivity_factor = 0.7 * good_comments + 0.3 * thumbs_up
        return self.views * time_factor * positivity_factor


class Interaction(models.Model):
    is_positive = models.BooleanField()
    time = models.DateTimeField(blank=True)


class Thumb(Interaction):
    video = models.ForeignKey(Video, related_name='thumbs', on_delete=models.CASCADE)
    pass


class Comment(Interaction):
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    pass
