from django.db import models
import uuid
import django.utils.timezone
from django.utils import timezone
import order
from django.db.models import Q

# Create your models here.
class Coupon(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    code = models.CharField(max_length=100, unique=True)
    discount_type = models.CharField(max_length = 30, choices = [('flat','flat'),('percentage','percentage')])
    discount = models.DecimalField(max_digits=5, decimal_places=2) #percentage
    from_date = models.DateField(default=django.utils.timezone.now)
    to_date = models.DateField()
    image = models.ImageField(upload_to="coupon/image",null = True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default = True)
    is_expired = models.BooleanField(default = False)
    limit = models.PositiveIntegerField()
    description = models.CharField(max_length = 4000,null = True,blank = True)

    @property
    def is_verify(self):
        return True #a user can use coupon one time only hints Order.objects.filter(user = request.user , coupons = coupon_obj.first()).exists() == False 
    
    @property
    def is_coupon_ok(self):
        now = timezone.now().date()
        return self.is_active and self.from_date <= now <= self.to_date and order.models.Order.objects.filter(coupons = self).filter(~Q(order_status='checkout')).count()<=self.limit


    