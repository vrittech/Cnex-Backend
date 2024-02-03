from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=255)

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length = 2000)

class Variation(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length = 1000)

class VariationOption(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    variations = models.ManyToManyField(Variation, through='ProductVariation')
    total_quantity = models.PositiveIntegerField(default=0)  # Total quantity for all variations
    brand = models.CharField(max_length=255)
    collection = models.ManyToManyField(Collection,related_name="products")

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_options = models.ManyToManyField(VariationOption)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # Quantity for this specific variation

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)

class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.CharField(max_length=255)
    date = models.DateField()
    time_slot = models.CharField(max_length=255)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=255, choices=[
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
        ('fonepay', 'FonePay'),
    ])

class BookedAppointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    cancellation_reason = models.TextField(null=True, blank=True)
