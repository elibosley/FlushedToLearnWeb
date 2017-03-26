from django import forms
from audioselector.models import MusicFile


class MediaForm(forms.ModelForm):
    class Meta:
        model = MusicFile
        fields = ('media',)


class UrlForm(forms.Form):
    url = forms.CharField(label='Video Url', max_length=1000)