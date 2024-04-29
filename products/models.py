from django.db import models
from variations.models import Variation,VariationOption
import uuid
from django.utils.text import slugify
import ast
from django.db.models import UniqueConstraint
from django.db.models import Sum

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
        # tag_names = tag_names.split(',')
        tag_names = ast.literal_eval(tag_names)
        tags = [Tags.objects.get_or_create(name=tag)[0] for tag in tag_names]
        return tags

class Collection(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length = 2000,null = True,blank = True)
    is_active = models.BooleanField(default = True)

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

    order_at = models.PositiveIntegerField(default = 1)

    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate the slug when saving the product if it's blank
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True) #editable=False
    name = models.CharField(max_length=5000)
    title = models.CharField(max_length = 2000,null = True)
    slug = models.SlugField(unique = True,blank=True,max_length = 5000)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits = 10,decimal_places=2,default = 0)
    product_type = models.CharField(max_length = 20, choices = (('pre-order','Pre Order'),('regular','Regular')),default = 'regular')
    is_manage_stock = models.BooleanField(default = False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null = True)
    quantity = models.PositiveIntegerField(default=0) 
    brand = models.ForeignKey(Brand,related_name = "products",on_delete = models.SET_NULL,null = True)
    is_best_sell = models.BooleanField(default = False)
    collection = models.ManyToManyField(Collection,related_name="products",blank=True)
    is_publish = models.BooleanField(default = True)

    is_stock =  models.BooleanField(default = True) #true means in stock, false means out of stocks
    
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

    @property
    def has_variations(self):
        return self.variations.all().exists()
    
    @property
    def total_sale(self):
        return self.order_items.all().count()

    @property
    def average_rating(self):
        total_rating = self.rating.all()
        if total_rating.exists():
            total_rating = int(total_rating.aggregate(total_rating=Sum('rating'))['total_rating'])
            return total_rating/self.rating.all().count()
        else:
            return 0
     
    
    @property
    def total_rating(self):
        return self.rating.all().count()
    
    @property
    def initial_quantity(self):
        return self.order_items.all().count()+self.quantity
    
    @property
    def total_variations_quantity(self):
        return 20
    
    def getPriceByvariation(self,variation_value):
        if self.variations.all().filter(variation_options = variation_value).exists():
            price = self.variations.all().filter(variation_options = variation_value).first().price#.filter(variation_options__in = variation_value)
            return price
        
        else:
            return 0
    
    def getPriceByvariationList(self,variation_value_list): #total price for single prouct,blunder
        price = self.variations.all().filter(variation_options__in=variation_value_list).aggregate(total_price=Sum('price'))['total_price']#.filter(variation_options__in = variation_value)
        total_price = float(price)+float(self.price) - float(self.discount)
        return total_price
    
    def getvariationPriceOnly(self,variation_value_list): #variation_price only for a product
        price = self.variations.all().filter(variation_options__in=variation_value_list).aggregate(total_price=Sum('price'))['total_price']#.filter(variation_options__in = variation_value)
        total_price = float(price)
        return total_price
    
    def getDetailWithVariationList(self,variation_value_list):
        product_detail_after_variations = self.variations.all().filter(variation_options__in=variation_value_list)
        
        variations = []
        variation_price = 0.00

        for pdav in product_detail_after_variations:
            variations_value = {
                'price':pdav.price,
                'value':pdav.variation_options.value

            }
          
            variation_price = float(pdav.price)+variation_price
            variations.append(variations_value)

        data = {
            'variations':variations,
            'name':self.name,
            'slug':self.slug,
            'price':self.price,
            'discount':self.discount,
            'product_price':self.price,
            'variation_price':variation_price
        }
        return data

class ProductHaveImages(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    product = models.ForeignKey(Product,related_name = "product_images",on_delete = models.CASCADE)
    image = models.ImageField(upload_to="products/images")

    def __str__(self):
        return str(self.product.name) + ":" + str(self.id)

class ProductDetailAfterVariation(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    product = models.ForeignKey(Product,related_name="variations", on_delete=models.CASCADE)
    variation_options = models.ForeignKey(VariationOption,on_delete = models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,default = 0)
    quantity = models.PositiveIntegerField(default=0)  # Quantity for this specific variation

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.name
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['variation_options', 'product'], name='unique_variation_product')
        ]