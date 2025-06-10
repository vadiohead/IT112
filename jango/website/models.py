from django.db import models

# Create your models here.

class SongList(models.Model):
    title = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    year = models.IntegerField()
    video = models.URLField()

    def __str__(self):
        return self.title
