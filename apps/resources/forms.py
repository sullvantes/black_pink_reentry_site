from django import forms
from models import Resource

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


