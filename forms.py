from django import forms
from .models import asset
from datetime import datetime

class AssetForm(forms.ModelForm):

    class Meta:
        model = asset
        fields = ['Name', 'Location', 'Subject', 'Value', 'AssetImage'] #'__all__' for all