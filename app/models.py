from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    certificate = models.FileField(upload_to='certificates/')
    social_media_alias = models.CharField(max_length=255)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    
    

