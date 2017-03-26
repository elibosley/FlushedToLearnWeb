import os

from django.conf import settings
from django.db import models


# Create your models here.

def uploaded_song_file_name(instance, filename):
    mp3name = 'uploaded_song.mp3'
    fullname = os.path.join(settings.MEDIA_ROOT, mp3name)
    if os.path.exists(fullname):
        os.remove(fullname)
    return mp3name


class MusicFile(models.Model):
    media = models.FileField(upload_to=uploaded_song_file_name)
