# forms.py
from django import forms
from .models import *

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['name', 'phone', 'email']