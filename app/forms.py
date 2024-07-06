from django import forms
from .models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields= ('name', 'certificate', 'social_media_alias', 'owner')