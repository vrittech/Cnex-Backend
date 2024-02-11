from django.db import models
from accounts.models import CustomUser
from variations.models import VariationGroup,VariationOption
import uuid
from django.utils.text import slugify

class Brand(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length = 200)
    description =  models.CharField(max_length = 2000)
    
    def __str__(self):
        return self.name

class Collection(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length = 2000)
    is_active = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique = True,blank=True)
    parent = models.ForeignKey("Category",related_name = "child",blank=True,null=True,on_delete = models.CASCADE)
    descrirption = models.CharField(max_length = 2000)
    image = models.ImageField(upload_to="category/images")
    variation_group = models.ForeignKey(VariationGroup,related_name = "category",null = True,on_delete = models.SET_NULL)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate the slug when saving the product if it's blank
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True) #editable=False
    name = models.CharField(max_length=255)
    title = models.CharField(max_length = 500,null = True)
    slug = models.SlugField(unique = True,blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0) 
    brand = models.ForeignKey(Brand,related_name = "products",on_delete = models.SET_NULL,null = True)
    is_best_sell = models.BooleanField(default = False)
    collection = models.ManyToManyField(Collection,related_name="products")
    is_publish = models.BooleanField(default = False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate the slug when saving the product if it's blank
        if not self.slug:
            self.slug = slugify(self.name)+'-'+str(self.public_id)[1:5] + str(self.public_id)[-1:-5]
        super().save(*args, **kwargs)


class ProductHaveImages(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    product = models.ForeignKey(Product,related_name = "product_images",on_delete = models.CASCADE)
    image = models.ImageField(upload_to="products/images")

    def __str__(self):
        return str(self.product.name) + ":" + str(self.id)

class ProductDetailAfterVariation(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_options = models.ManyToManyField(VariationOption)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # Quantity for this specific variation
    
    def __str__(self):
        return self.product.name

class Rating(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.CharField(max_length = 2000,default = "")

    def __str__(self) -> str:
        return str(self.user.username)+" "+str(self.product) +":"+ str(self.rating)




#variation are based on category, we have to define each category with variation group.
    
#each category have any one of variation group.
#variation group are collection of attribute, each group have multiple variation
#attributes are value