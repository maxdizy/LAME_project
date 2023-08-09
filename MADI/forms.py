from django.forms import ModelForm
from django import forms
from .models import config

class uploadForm(ModelForm):
    caseNo = forms.TextInput()
    dart = forms.BooleanField(required=False)
    mod = forms.BooleanField(required=False)
    class Meta:
        model = config
        fields = ['caseNo', 'dart', 'mod']