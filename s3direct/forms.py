# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class LocalUploadForm(forms.Form):
    key = forms.CharField()
    file = forms.FileField()
