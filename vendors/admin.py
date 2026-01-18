from django.contrib import admin
from .models import Vendor, Market, MarketApplicant, Rating, Blog, Notification


class VendorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "social_media_alias",
        "ssm_no",
        "product_name",
        "product_type",
        "product_picture",
        "menu",
    )


class MarketAdmin(admin.ModelAdmin):
    list_display = ("date",)


class MarketApplicantAdmin(admin.ModelAdmin):
    list_display = (
        "market",
        "vendor",
        "slot",
        "certificate",
        "equipment_list",
        "approved",
        "proof_of_payment",
        "booth_no",
    )


class RatingAdmin(admin.ModelAdmin):
    list_display = ("vendor", "rating", "comment")


class BlogAdmin(admin.ModelAdmin):
    list_display = ("vendor", "title", "content")


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("vendor", "message", "read", "created_at")


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Market, MarketAdmin)
admin.site.register(MarketApplicant, MarketApplicantAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Notification, NotificationAdmin)
