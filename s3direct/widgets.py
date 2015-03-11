# coding=utf-8
from __future__ import unicode_literals
import os
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.conf import settings


HTML = (
    '<div class="s3direct" data-url="{policy_url}">'
    '  <div class="link-controls">'
    '    <a class="link" target="_blank" href="{file_url}">{file_name}</a>'
    '    <a class="remove" href="#remove">Очистить</a>'
    '  </div>'
    '  <div class="progress-controls">'
    '    <div class="progress progress-striped">'
    '        <div class="progress-bar progress-bar-success" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">'
    '        </div>'
    '        <div class="info"></div>'
    '    </div>'
    '    <span class="abort btn btn-danger btn-sm">Отмена</span>'
    '  </div>'
    '  <div class="form-controls">'
    '    <input type="hidden" value="{file_url}" id="{element_id}" name="{name}" />'
    '    <input type="file" class="fileinput" />'
    '  </div>'
    '</div>'
)


class S3DirectEditor(widgets.TextInput):
    class Media:
        js = (
            's3direct/js/jquery-1.10.2.min.js',
            's3direct/js/jquery.iframe-transport.js',
            's3direct/js/jquery.ui.widget.js',
            's3direct/js/jquery.fileupload.js',
            's3direct/js/s3direct.js',
        )
        css = {
            'all': (
                's3direct/css/bootstrap-progress.min.css',
                's3direct/css/styles.css',
            )
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        super(S3DirectEditor, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        element_id = final_attrs.get('id')
        kwargs = {'upload_to': self.upload_to}

        policy_url = reverse('s3direct', kwargs=kwargs)
        file_url = value if value else ''
        if hasattr(file_url, 'name'):
            file_url = file_url.name
        file_name = os.path.basename(file_url)

        output = HTML.format(policy_url=policy_url,
                             file_url=file_url,
                             file_name=file_name,
                             element_id=element_id,
                             name=name)

        return mark_safe(output)
