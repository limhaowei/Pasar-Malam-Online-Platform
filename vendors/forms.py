from django import forms
from .models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields= ('name', 'phone_number', 'social_media_alias', 'ssm_no', 'product_name', 'product_type', 'certificate', 'product_picture', 'menu', 'equipment')