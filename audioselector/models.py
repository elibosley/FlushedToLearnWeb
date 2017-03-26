import os

from django.conf import settings
from django.db import models


# Create your models here.

def uploaded_song_file_name(instance, filename):
    fullname = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(fullname):
        os.remove(fullname)
    return filename


class MusicFile(models.Model):
    media = models.FileField(upload_to=uploaded_song_file_name)
    selected = models.BooleanField(default=False)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
