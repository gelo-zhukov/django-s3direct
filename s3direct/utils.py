# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import os
import urllib
import uuid
from base64 import b64encode
from datetime import datetime, timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from s3direct import defaults


def create_upload_data(content_type, source_filename, upload_to):
    if defaults.S3DIRECT_UNIQUE_RENAME:
        extension = os.path.splitext(source_filename)[1]
        filename = force_text(uuid.uuid4()) + extension
    else:
        filename = source_filename

    file_path = "%s/%s" % (upload_to, filename)

    content_disposition = 'attachment; filename="%s"' % urllib.quote(
        source_filename.encode('utf-8'))

    # local upload fallback
    if not getattr(settings, 'AWS_SECRET_ACCESS_KEY', None):
        return {
            "form_action": reverse('s3direct_local_upload'),
            "file_path": file_path,

            "key": file_path,  # will be used in local form
            "Content-Type": content_type,  # just in case
            "Content-Disposition": content_disposition  # just in case
        }

    access_key = settings.AWS_ACCESS_KEY_ID
    secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    bucket = settings.AWS_STORAGE_BUCKET_NAME
    endpoint = settings.S3DIRECT_ENDPOINT

    expires_in = datetime.now() + timedelta(hours=24)
    expires = expires_in.strftime('%Y-%m-%dT%H:%M:%S.000Z')

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

    key = "%s/%s/%s" % (defaults.S3DIRECT_ROOT_DIR, upload_to, filename)
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
