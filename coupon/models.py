from django.db import models
import uuid
import django.utils.timezone

# Create your models here.
class Coupon(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    code = models.CharField(max_length=100, unique=True)
    discount_type = models.CharField(max_length = 30, choices = [('flat','percentage')])
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    discount_amount = models.FloatField()
    from_date = models.DateField(default=django.utils.timezone.now)
    to_date = models.DateField()
    image = models.ImageField(upload_to="coupon/image")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    