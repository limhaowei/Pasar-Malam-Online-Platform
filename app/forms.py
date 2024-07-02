from django import forms
from .models import Registration, Review

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ('vendor', 'certificate', 'social_media_alias')


        
        
        
        