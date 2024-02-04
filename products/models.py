from django.db import models
from accounts.models import CustomUser

class Brand(models.Model):
    name = models.CharField(max_length = 200)
    description =  models.CharField(max_length = 2000)
    
    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length = 2000)
    
    def __str__(self):
        return self.name

class Variation(models.Model): #color
    name = models.CharField(max_length=255)
    description = models.CharField(max_length = 1000)

    def __str__(self):
        return self.name

class VariationOption(models.Model): #red,green
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.variation.name)+":" + str(self.value)  

class VariationGroup(models.Model): #electronics variation
    name = models.CharField(max_length = 50)
    variations = models.ManyToManyField(Variation,related_name="variation_group")

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("Category",related_name = "child",null=True,on_delete = models.CASCADE)
    descrirption = models.CharField(max_length = 2000)
    variation_group = models.ForeignKey(VariationGroup,related_name = "category",null = True,on_delete = models.SET_NULL)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0) 
    brand = models.ForeignKey(Brand,related_name = "products",on_delete = models.SET_NULL,null = True)
    collection = models.ManyToManyField(Collection,related_name="products")

    
    def __str__(self):
        return self.name

class ProductHaveImages(models.Model):
    product = models.ForeignKey(Product,related_name = "product_images",on_delete = models.CASCADE)
    image = models.ImageField(upload_to="products/images")

    def __str__(self):
        return str(self.product.name) + ":" + str(self.id)

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_options = models.ManyToManyField(VariationOption)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # Quantity for this specific variation
    
    def __str__(self):
        return self.product.name

class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.CharField(max_length = 2000,default = "")

    def __str__(self) -> str:
        return str(self.user.username)+" "+str(self.product) +":"+ str(self.rating)

class Slots(models.Model): #time #by admin
    time_slot = models.CharField(max_length=255) #by admin, time slot list by admin
    number_of_staffs = models.IntegerField()
    date = models.DateField() #by admin, date list by admin
    
    def __str__(self) -> str:
        return str(self.time_slot) +" , "+ str(self.number_of_staffs) + " staff"

class Services(models.Model): #by admin
    name =  models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    slots = models.ManyToManyField(Slots) #if number of slots reached then, it raise errors slots not available.
    
    def __str__(self) -> str:
        return self.name + " " + str(self.price)

class Appointment(models.Model): #by users
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ManyToManyField(Services,related_name="Appointment") #Multiple servies, each services has price
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=255, choices=[
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
        ('fonepay', 'FonePay'),
    ])

    def __str__(self) -> str:
        return self.user.username + " " + str(self.service.first().name)

class BookedAppointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    cancellation_reason = models.TextField(null=True, blank=True)


#variation are based on category, we have to define each category with variation group.
    
#each category have any one of variation group.
#variation group are collection of attribute, each group have multiple variation
#attributes are value