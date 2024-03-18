from django.db import models
from accounts.models import CustomUser
from variations.models import Variation,VariationOption
import uuid
from django.utils.text import slugify

class Brand(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length = 200)
    description =  models.CharField(max_length = 2000)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Tags(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class TagManager(models.Manager):
    def get_or_create_tags(self, tag_names):
        # Create or retrieve Tag objects based on tag names
        print(tag_names)
        # tag_names = tag_names.split(',')
        tags = [Tags.objects.get_or_create(name=tag)[0] for tag in tag_names]
        return tags

class Collection(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length = 2000,null = True,blank = True)
    is_active = models.BooleanField(default = False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique = True,blank=True)
    parent = models.ForeignKey("Category",related_name = "childs",blank=True,null=True,on_delete = models.CASCADE)
    descrirption = models.CharField(max_length = 2000,null = True,blank = True)
    image = models.ImageField(upload_to="category/images",null=True)
    variations = models.ManyToManyField(Variation,related_name = "category",blank= True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

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
    discount = models.DecimalField(max_digits = 10,decimal_places=2,null = True)
    product_type = models.CharField(max_length = 20, choices = (('pre-order','Pre Order'),('regular','Regular')),default = 'regular')
    is_manage_stock = models.BooleanField(default = False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0) 
    brand = models.ForeignKey(Brand,related_name = "products",on_delete = models.SET_NULL,null = True)
    is_best_sell = models.BooleanField(default = False)
    collection = models.ManyToManyField(Collection,related_name="products")
    is_publish = models.BooleanField(default = False)
    
    tags = models.ManyToManyField(Tags,blank=True)

    variation_options = models.ManyToManyField(VariationOption, through='ProductDetailAfterVariation')

    objects = models.Manager()
    tag_manager = TagManager() 

    featured_image = models.ImageField(upload_to="products/featured_image/images",null=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate the slug when saving the product if it's blank
        if not self.slug:
            self.slug = slugify(self.name)+'-'+str(self.public_id)[1:5] + str(self.public_id)[-1:-5]
        super().save(*args, **kwargs)

    def save_tags(self, tag_names):
        tags = Product.tag_manager.get_or_create_tags(tag_names)
        self.tags.set(tags)

class ProductHaveImages(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    product = models.ForeignKey(Product,related_name = "product_images",on_delete = models.CASCADE)
    image = models.ImageField(upload_to="products/images")

    def __str__(self):
        return str(self.product.name) + ":" + str(self.id)

class ProductDetailAfterVariation(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    product = models.ForeignKey(Product,related_name="variations", on_delete=models.CASCADE)
    variation_options = models.OneToOneField(VariationOption,on_delete = models.PROTECT,)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)  # Quantity for this specific variation

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name

class Rating(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.CharField(max_length = 2000,default = "")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user.username)+" "+str(self.product) +":"+ str(self.rating)




#variation are based on category, we have to define each category with variation group.
    
#each category have any one of variation group.
#variation group are collection of attribute, each group have multiple variation
#attributes are value