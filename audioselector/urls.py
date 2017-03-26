from django.conf.urls import url

from audioselector import views

urlpatterns = [
    url(r'upload$', views.model_form_upload, name="upload_form"),
    url(r'info.json$', views.get_information, name="get_information")
    # get information about the selected song to play
]
