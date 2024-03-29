from django.db import models
from django.core.validators import MaxValueValidator
from accounts.models import CustomUser
import uuid
from products.models import Product
# Create your models here.


class Rating(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.ForeignKey(CustomUser,related_name = "rating", on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name = "rating", on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    
    message = models.TextField(null = True)
    image = models.ImageField(null=True,upload_to="review/images")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user.username)+" "+str(self.product) +":"+ str(self.rating)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_rating')
        ]
        

class AppRating(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    user = models.OneToOneField(CustomUser,related_name = "apprating", on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(validators=[MaxValueValidator(4)])
    
    message = models.TextField(null = True)
    image = models.ImageField(null=True,upload_to="review/images")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user.username)+" "+str(self.product) +":"+ str(self.rating)
    
        