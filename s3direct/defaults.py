#coding=utf-8
from __future__ import unicode_literals
from django.conf import settings

S3DIRECT_UNIQUE_RENAME = getattr(settings, "S3DIRECT_UNIQUE_RENAME", None)
S3DIRECT_ROOT_DIR = getattr(settings, "S3DIRECT_ROOT_DIR", '')
