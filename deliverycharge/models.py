from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class DeliveryCharge(models.Model):#if order price falls between min and max then delivery free and delivery charge. validate min and max,so there must be single
    min_price = models.PositiveIntegerField()
    max_price = models.PositiveIntegerField()
    is_delivery_free = models.BooleanField(default = False)
    delivery_charge = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_delivery_charge(self):
     
        charges = self
        if charges.is_delivery_free:
            return {
                'delivery_charge':charges.delivery_charge,
                'is_delivery_free':charges.is_delivery_free,
                'min_price':charges.min_price,
                'max_price':charges.max_price,
                'total_delivery_charge':0
            }
        else:
            return {
                'delivery_charge':charges.delivery_charge,
                'is_delivery_free':charges.is_delivery_free,
                'min_price':charges.min_price,
                'max_price':charges.max_price,
                'total_delivery_charge':charges.delivery_charge
            }
        
       
    def clean(self):
        # Check if there are any existing records that overlap with the current price range
        overlapping_ranges = DeliveryCharge.objects.exclude(id=self.id).filter(
            min_price__lt=self.max_price,
            max_price__gt=self.min_price
        )

        if overlapping_ranges.exists():
            raise ValidationError("Price range overlaps with existing records.")
        
        if self.max_price<=self.min_price:
            raise ValidationError("max price range must be greater than min price range.")


    def save(self, *args, **kwargs):
        self.clean()  # Run the clean method to validate the object before saving
        super().save(*args, **kwargs)