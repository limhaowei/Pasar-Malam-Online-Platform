from django.contrib import admin
from .models import Vendor

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'certificate', 'social_media_alias', 'owner')
    


admin.site.register(Vendor, VendorAdmin)