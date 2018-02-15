from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Video(models.Model):
    title = models.CharField(max_length=50, unique=True)
    date_uploaded = models.DateTimeField(blank=True)
    views = models.IntegerField(default=0)
    themes = models.ManyToManyField(Theme)
