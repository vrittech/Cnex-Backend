from django.db import models
from accounts.models import CustomUser,ShippingAddress
from products.models import ProductDetailAfterVariation,Product
from variations.models import  VariationOption
from coupon.models import Coupon
import uuid
from django.db.models import UniqueConstraint

# Create your models here.
class Order(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser,related_name = "orders", on_delete=models.PROTECT)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2,default = 0)#
    is_delivery_free = models.BooleanField(default = False) 
    delivery_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    coupons = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    quantity =  models.PositiveIntegerField(default = 1)
    total_discount = models.PositiveIntegerField(default = 0)
    payment_status= models.CharField(max_length=255, choices=[
        ('paid','Paid'),
        ('unpaid','unpaid'),
        ('half', 'Half Payment'),
        ('cod','Cash On Delivery'),
        ('refunded','Refunded'),
    ],default = 'cod')
    order_status = models.CharField(max_length=255, choices=[
        ('in-progress', 'In Progress'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
        ('shipped','shipped'),
        ('checkout','checkout')
    ])
    order_date = models.DateTimeField(auto_now_add=True)
    
     
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'coupons'], name='limit_coupon')
        ]

class OrderItem(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    order = models.ForeignKey(Order,related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items', on_delete=models.SET_NULL,null = True)
    variations = models.ManyToManyField(VariationOption,related_name='order_items',blank=True)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default = 0)
    total_price = models.PositiveIntegerField(default = 0)
    discount = models.PositiveIntegerField(default = 0)
    variations_price = models.PositiveIntegerField(default = 0)
    price_with_variation = models.PositiveBigIntegerField(default= 0)

class Wishlist(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.OneToOneField(CustomUser,related_name="wishlists", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

class Cart(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_date = models.DateTimeField(auto_now_add=True)
    
    product = models.ForeignKey(Product,related_name='carts', on_delete=models.CASCADE)
    variations = models.ManyToManyField(VariationOption,related_name='carts',blank = True)
    quantity = models.PositiveIntegerField()

# class Checkout(models.Model):
#     public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     carts = models.ManyToManyField(Cart,related_name="checkout")
    


    
    
