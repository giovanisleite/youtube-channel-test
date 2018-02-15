from django.db import models
from django.utils import timezone


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Video(models.Model):
    title = models.CharField(max_length=50, unique=True)
    date_uploaded = models.DateTimeField(blank=True)
    views = models.IntegerField(default=0)
    themes = models.ManyToManyField(Theme)

    @property
    def score(self):
        days_since_upload = (timezone.now() - self.date_uploaded).days
        time_factor = max(0, 1 - days_since_upload/365)

        good_comments = self.comments.filter(is_positive=True).count()/self.comments.count()
        thumbs_up = self.thumbs.filter(is_positive=True).count()/self.thumbs.count()
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
