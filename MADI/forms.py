from django.forms import ModelForm
from django import forms
from .models import config, IRFdata
from LAME.settings import get_file

class uploadForm(ModelForm):
    caseNo = forms.TextInput()
    ERFpath = forms.TextInput()
    dart = forms.BooleanField(required=False)
    mod = forms.BooleanField(required=False)
    class Meta:
        model = config
        fields = ['caseNo', 'ERFpath', 'dart', 'mod']

    def __init__(self, *args, **kwargs):
        super(uploadForm, self).__init__(*args, **kwargs)
        self.fields["ERFpath"].initial = get_file('data/ERFL.txt').read().decode()