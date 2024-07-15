from django.core.signals import request_started
from django.dispatch import receiver
from .models import MarketApplicant, Notification
from .services import NotificationService

@receiver(request_started)
def send_notification_on_approval(sender, **kwargs):
    if 'market_applicant' in kwargs:
        market_applicant = kwargs['market_applicant']
        if market_applicant.approved:
            notification_service = NotificationService()
            notification_service.send_notification(market_applicant.vendor, 'Your application has been approved!')
            
            
            
            