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

    def clean(self):
        # Check if there are any existing records that overlap with the current price range
        overlapping_ranges = DeliveryCharge.objects.filter(
            min_price__lt=self.max_price,
            max_price__gt=self.min_price
        ).exclude(pk=self.pk)

        if overlapping_ranges.exists():
            raise ValidationError("Price range overlaps with existing records.")

    def save(self, *args, **kwargs):
        self.clean()  # Run the clean method to validate the object before saving
        super().save(*args, **kwargs)