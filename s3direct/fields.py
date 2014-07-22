from django.db.models import Field, FileField
from django.db.models.fields.files import FileDescriptor
from s3direct.widgets import S3DirectEditor
from django.conf import settings


if hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
    class S3DirectField(Field):
        descriptor_class = FileDescriptor

        def __init__(self, *args, **kwargs):
            upload_to = kwargs.pop('upload_to', '')
            self.widget = S3DirectEditor(upload_to=upload_to)
            kwargs['max_length'] = kwargs.get('max_length', 100)
            super(S3DirectField, self).__init__(*args, **kwargs)

        def get_internal_type(self):
            return "TextField"

        def formfield(self, **kwargs):
            defaults = {'widget': self.widget}
            defaults.update(kwargs)
            return super(S3DirectField, self).formfield(**defaults)
else:
    class S3DirectField(FileField):
        pass


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^s3direct\.fields\.S3DirectField"])