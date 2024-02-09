from django.db import models
import uuid
# Create your models here.
class Coupon(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiry_date = models.DateField()