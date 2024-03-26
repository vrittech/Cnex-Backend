from django.db import models

# Create your models here.

class DeliveryCharge(models.Model):
    min_price = models.PositiveIntegerField()
    max_price = models.PositiveIntegerField()
    is_delivery_free = models.BooleanField(default = False)
    delivery_charge = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)