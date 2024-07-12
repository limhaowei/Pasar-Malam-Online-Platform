from django.contrib import admin
from .models import Vendor

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'social_media_alias', 'ssm_no', 'product_name', 'product_type', 'certificate', 'product_picture', 'menu', 'equipment')
    


admin.site.register(Vendor, VendorAdmin)