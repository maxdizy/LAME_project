from django.forms import ModelForm
from django import forms
from .models import config, IRFdata
from LAME import settings

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
        self.fields["ERFpath"].initial = settings.get_file('data/ERFL.txt').read().decode()

class IRFdataForm(ModelForm):
    CN = forms.TextInput()
    tail = forms.TextInput()
    IRFTitle = forms.TextInput()
    description = forms.TextInput()
    affected = forms.TextInput()
    IRFNo = forms.TextInput()
    ROED = forms.BooleanField()
    dart = forms.BooleanField()
    mod = forms.BooleanField()
    fileName = forms.TextInput()
    class Meta:
        model = IRFdata
        fields = ['CN', 'tail', 'IRFTitle', 'description', 'affected', 'IRFNo', 'ROED', 'dart', 'mod', 'fileName']

    def __init__(self, CN, tail, IRFTitle, description, affected, IRFNo, ROED, dart, mod, fileName, *args, **kwargs):
        super(IRFdataForm, self).__init__(*args, **kwargs)
        self.fields["CN"].initial = CN
        self.fields["tail"].initial = tail
        self.fields["IRFTitle"].initial = IRFTitle
        self.fields["description"].initial = description
        self.fields["affected"].initial = affected
        self.fields["IRFNo"].initial = IRFNo
        self.fields["ROED"].initial = ROED
        self.fields["dart"].initial = dart
        self.fields["mod"].initial = mod
        self.fields["fileName"].initial = fileName
