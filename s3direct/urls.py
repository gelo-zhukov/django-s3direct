from django.conf.urls import url
from s3direct.views import get_upload_params, local_upload_view

urlpatterns = [
    url('^get_upload_params/(?P<upload_to>.*)', get_upload_params, name='s3direct'),
    url('^local_upload/$', local_upload_view, name='s3direct_local_upload'),
]
