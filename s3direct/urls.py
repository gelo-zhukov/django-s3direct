from django.conf.urls import url
from s3direct.views import get_upload_params, LocalUploadView

urlpatterns = [
    url('^get_upload_params/', get_upload_params, name='s3direct'),
    url('^local_upload/', LocalUploadView.as_view(), name='s3direct_local_upload'),
]
