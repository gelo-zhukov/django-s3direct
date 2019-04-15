from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^s3direct/', include('s3direct.urls')),
    url(r'^form/', include('cat.urls')),
]
