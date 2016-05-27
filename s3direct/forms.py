from django import forms


class LocalUploadForm(forms.Form):
    key = forms.CharField()
    file = forms.FileField()
