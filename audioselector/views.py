import os

import boto3
import youtube_dl
from django.conf import settings
from django.core.mail.backends import console
from django.shortcuts import render, redirect

# Create your views here.
from audioselector.forms import MediaForm, UrlForm
from audioselector.models import MusicFile


def online_song_file_name():
    mp3name = "online_song.mp3"
    fullname = os.path.join(settings.MEDIA_ROOT, mp3name)
    if os.path.exists(fullname):
        os.remove(fullname)

    return fullname


client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
bucket = settings.AWS_STORAGE_BUCKET_NAME


def upload(d):
    filename = "online_song.mp3"
    filepath = os.path.join(settings.MEDIA_ROOT, "online_song.mp3")
    client.upload_file(filepath, bucket, filename)
    client.put_object_acl(ACL='public-read', Bucket=bucket, Key=filename)
    region = "us-east-1"
    return "https://s3-%s.amazonaws.com/{0}/{1}".format(region, bucket, filename)


def model_form_upload(request):
    if request.method == 'POST':
        url_form = UrlForm(request.POST)

        if url_form.is_valid():
            # Do youtube stuff
            options = {
                'format': 'bestaudio/best',  # choice of quality
                'extractaudio': True,  # only keep the audio
                'audioformat': "mp3",  # convert to mp3
                'outtmpl': '%(id)s',  # name the file the ID of the video
                'noplaylist': True,  # only download single song, not playlist
            }
            ydl = youtube_dl.YoutubeDL(options)
            r = None
            url = url_form.cleaned_data['url']
            print(url)
            with ydl:
                file = ydl.extract_info(url, download=True)  # don't download, much faster

                print(file['id'])
                if (os.path.exists(os.path.join(settings.MEDIA_ROOT, "online_song.mp3"))):
                    os.remove(os.path.join(settings.MEDIA_ROOT, "online_song.mp3"))
                os.rename(file['id'], os.path.join(settings.MEDIA_ROOT, "online_song.mp3"))
                upload(file)

            return redirect(model_form_upload)
    else:
        url_form = UrlForm()
    return render(request, 'simple_upload.html', {
        'url_form': url_form
    })
