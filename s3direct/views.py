# -*- coding: utf-8 -*-
import json
import os

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from s3direct.forms import LocalUploadForm
from s3direct.utils import create_upload_data


@csrf_exempt
@require_POST
def get_upload_params(request, upload_to=''):
    content_type = request.POST.get('type', 'application/octet-stream')
    source_filename = request.POST['name']
    data = create_upload_data(content_type, source_filename, upload_to)
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
@require_POST
def local_upload_view(request):
    form = LocalUploadForm(request.POST, request.FILES)
    if form.is_valid():
        path = os.path.join(settings.MEDIA_ROOT, form.cleaned_data['key'])
        content = form.cleaned_data['file']
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path, 'wb+') as opened:
            for chunk in content.chunks():
                opened.write(chunk)
    return HttpResponse(status=201)
