from django import forms
from .models import Vendor, MarketApplicant


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            "name",
            "phone_number",
            "social_media_alias",
            "ssm_no",
            "product_name",
            "product_type",
            "product_picture",
            "menu",
        ]


class MarketApplicantForm(forms.ModelForm):
    class Meta:
        model = MarketApplicant
        fields = ["slot", "certificate", "equipment_list"]


class VendorPageForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = [
            "name",
            "social_media_alias",
        ]
