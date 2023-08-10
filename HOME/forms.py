from django.forms import ModelForm
from django import forms
from .models import contact

class contactAdminForm(ModelForm):
    ID = forms.TextInput()
    email = forms.TextInput()
    type = forms.TextInput()
    body = forms.TextInput()
    class Meta:
        model = contact
        fields = ['ID', 'email', 'type', 'body']