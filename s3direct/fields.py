from django.core.files.storage import default_storage
from django.db.models import FileField
from django.db.models.fields import TextField
from django.db.models.fields.files import FileDescriptor, FieldFile
from s3direct.widgets import S3DirectEditor
from django.conf import settings


if hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
    class S3DirectField(TextField):

        attr_class = FieldFile
        descriptor_class = FileDescriptor

        def __init__(self, storage=None, *args, **kwargs):
            self.storage = storage or default_storage
            upload_to = kwargs.pop('upload_to', '')
            self.widget = S3DirectEditor(upload_to=upload_to)
            kwargs['max_length'] = kwargs.get('max_length', 100)
            super(S3DirectField, self).__init__(*args, **kwargs)

        def formfield(self, **kwargs):
            defaults = {'widget': self.widget}
            defaults.update(kwargs)
            return super(S3DirectField, self).formfield(**defaults)

        def contribute_to_class(self, cls, name, virtual_only=False):
            super(S3DirectField, self).contribute_to_class(cls, name, virtual_only)
            setattr(cls, self.name, self.descriptor_class(self))
else:
    class S3DirectField(FileField):
        pass


if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^s3direct\.fields\.S3DirectField"])