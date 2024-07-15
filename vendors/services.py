from django.core.signals import request_started
from django.dispatch import receiver
from .models import Notification


class NotificationService:
    def send_notification(self, vendor, message):
        notification = Notification(vendor=vendor, message=message)
        notification.save()

    def get_unread_notifications(self, vendor):
        return Notification.objects.filter(vendor=vendor, read=False)
    
    
    
    