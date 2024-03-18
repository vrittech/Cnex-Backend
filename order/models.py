from django.db import models
from accounts.models import CustomUser,ShippingAddress
from products.models import ProductDetailAfterVariation,Product
from coupon.models import Coupon
import uuid

# Create your models here.
class Order(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name = "order",on_delete = models.CASCADE)
    products_variations = models.ManyToManyField(ProductDetailAfterVariation, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    coupons = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status= models.CharField(max_length=255, choices=[
        ('paid','Paid'),
        ('half', 'Half Payment'),
        ('cod','Cash On Delivery'),
        ('refunded','Refunded'),
    ])
    order_status = models.CharField(max_length=255, choices=[
        ('in-progress', 'In Progress'),
        ('in-progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
        ('shipped','shipped')
    ])
    order_date = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductDetailAfterVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Wishlist(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

class Cart(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductDetailAfterVariation)