from django.core.signals import request_started
from django.dispatch import receiver
from .models import MarketApplicant, Notification, Vendor
from .services import NotificationService

from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User


@receiver(request_started)
def send_notification_on_approval(sender, **kwargs):
    if "market_applicant" in kwargs:
        market_applicant = kwargs["market_applicant"]
        if market_applicant.approved:
            notification_service = NotificationService()
            notification_service.send_notification(
                market_applicant.vendor, "Your application has been approved!"
            )


@receiver(post_save, sender=User)
def createVendor(sender, instance, created, **kwargs):
    if created:
        user = instance
        vendor = Vendor.objects.create(
            user=user,
            name=user.username,
        )


@receiver(post_save, sender=Vendor)
def updateUser(sender, instance, created, **kwargs):
    vendor = instance
    user = vendor.user

    if created == False:
        user.username = vendor.name
        user.save()


@receiver(post_delete, sender=Vendor)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
