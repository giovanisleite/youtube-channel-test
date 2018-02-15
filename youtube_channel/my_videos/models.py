from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Video(models.Model):
    title = models.CharField(max_length=50, unique=True)
    date_uploaded = models.DateTimeField(blank=True)
    views = models.IntegerField(default=0)
    themes = models.ManyToManyField(Theme)


class Interaction(models.Model):
    is_positive = models.BooleanField()
    time = models.DateTimeField(blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)


class Thumb(Interaction):
    pass

class Comment(Interaction):
    pass
