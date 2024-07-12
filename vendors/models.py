from django.db import models

class Vendor(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('F&B', 'F&B'),
        ('Non-F&B', 'Non-F&B'),
    ]
    
    name = models.CharField(max_length=255)
    phone_number = models.DecimalField(max_digits = 10, decimal_places = 0)
    social_media_alias = models.CharField(max_length=255)
    ssm_no = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)
    certificate = models.FileField(upload_to='certificates/')
    product_picture = models.ImageField(upload_to='product_pictures/')
    menu = models.FileField(upload_to='menus/')
    equipment = models.CharField(max_length=255)
    
    

# class MarketVendor(models.Model):
#     market = models.ForeignKey('Market', on_delete = models.CASCADE)
#     vendor = models.ForeignKey('Vendor', on_delete = models.CASCADE)
#     proof_of_payment = models.FileField(upload_to='proof_of_payments/', blank=True, null=True)
#     booth_no = models.CharField(max_length=255, blank=True, null=True)
     
# class Market(models.Model):
#     date = models.DateField()

     
     

    