import uuid
from django.core.files.storage import default_storage
from django.db.models import FileField
from django.db.models.fields import TextField
from django.db.models.fields.files import FileDescriptor, FieldFile
from s3direct import defaults
from s3direct.widgets import S3DirectEditor
from django.conf import settings


if hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
    class S3DirectField(TextField):

        attr_class = FieldFile
        descriptor_class = FileDescriptor

        def __init__(self, storage=None, *args, **kwargs):
            self.storage = storage or default_storage
            self.upload_to = kwargs.pop('upload_to', '')
            self.widget = S3DirectEditor(upload_to=self.upload_to)
            kwargs['max_length'] = kwargs.get('max_length', 100)
            super(S3DirectField, self).__init__(*args, **kwargs)

        def formfield(self, **kwargs):
            defaults = {'widget': self.widget}
            defaults.update(kwargs)
            return super(S3DirectField, self).formfield(**defaults)

        def contribute_to_class(self, cls, name, virtual_only=False):
            super(S3DirectField, self).contribute_to_class(cls, name, virtual_only)
            setattr(cls, self.name, self.descriptor_class(self))

        def generate_filename(self, instance, filename):
            if defaults.S3DIRECT_UNIQUE_RENAME:
                ext = filename.split('.')[-1]
                filename = '%s.%s' % (uuid.uuid4(), ext)
            else:
                filename = '${filename}'
            return "%s/%s/%s" % (defaults.S3DIRECT_ROOT_DIR, self.upload_to, filename)
else:
    class S3DirectField(FileField):
        pass
