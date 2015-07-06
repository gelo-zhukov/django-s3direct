#coding=utf-8
import hashlib
import uuid
import hmac
import json
import urllib
from datetime import datetime, timedelta
from base64 import b64encode
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from s3direct import defaults


@csrf_exempt
@require_POST
def get_upload_params(request, upload_to=''):
    content_type = request.POST.get('type', 'application/octet-stream')
    source_filename = request.POST['name']
    data = create_upload_data(content_type, source_filename, upload_to)
    return HttpResponse(json.dumps(data), content_type="application/json")


def create_upload_data(content_type, source_filename, upload_to):
    access_key = settings.AWS_ACCESS_KEY_ID
    secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    endpoint = settings.S3DIRECT_ENDPOINT

    expires_in = datetime.now() + timedelta(hours=24)
    expires = expires_in.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    content_disposition = 'attachment; filename="%s"' % urllib.quote(source_filename.encode('utf-8'))

    policy_object = json.dumps({
        "expiration": expires,
        "conditions": [
            {"bucket": bucket},
            {"acl": "public-read"},
            {"Content-Type": content_type},
            {"Content-Disposition": content_disposition},
            ["starts-with", "$key", ""],
            {"success_action_status": "201"}
        ]
    })

    policy = b64encode(policy_object.replace('\n', '').replace('\r', ''))
    signature = hmac.new(str(secret_access_key), policy, hashlib.sha1).digest()
    signature_b64 = b64encode(signature)

    if defaults.S3DIRECT_UNIQUE_RENAME:
        ext = source_filename.split('.')[-1]
        filename = '%s.%s' % (uuid.uuid4(), ext)
    else:
        filename = '${filename}'

    key = "%s/%s/%s" % (defaults.S3DIRECT_ROOT_DIR, upload_to, filename)
    file_path = "%s/%s" % (upload_to, filename)
    bucket_url = "https://%s/%s" % (endpoint, bucket)

    return {
        "form_action": bucket_url,
        "file_path": file_path,

        "policy": policy,
        "signature": signature_b64,
        "key": key,
        "AWSAccessKeyId": access_key,
        "success_action_status": "201",
        "acl": "public-read",
        "Content-Type": content_type,
        "Content-Disposition": content_disposition
    }
