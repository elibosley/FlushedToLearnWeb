import os

import youtube_dl
from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.
from audioselector.forms import MediaForm, UrlForm


def online_song_file_name():
    mp3name = 'online_song.mp3'
    fullname = os.path.join(settings.MEDIA_ROOT, mp3name)
    if os.path.exists(fullname):
        try:
            os.remove(fullname)
        except FileNotFoundError:
            print("File not found!")

    return fullname


def model_form_upload(request):
    if request.method == 'POST':
        upload_form = MediaForm(request.POST, request.FILES)
        url_form = UrlForm(request.POST)
        if upload_form.is_valid():
            upload_form.save()
            return redirect(model_form_upload)
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
            with ydl:
                r = ydl.extract_info(url, download=True)  # don't download, much faster
                os.rename(r['id'], online_song_file_name())

            # print some typical fields
            print(
                "%s was uploaded by '%s' and has %d views, %d likes, and %d dislikes" % (
                    r['title'], r['uploader'], r['view_count'], r['like_count'], r['dislike_count']))
            return redirect(model_form_upload)
    else:
        upload_form = MediaForm()
        url_form = UrlForm()
    return render(request, 'simple_upload.html', {
        'upload_form': upload_form,
        'url_form': url_form
    })
