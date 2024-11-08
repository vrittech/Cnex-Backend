from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from .roles import roles_data,roles_data_dict
from .import roles
import uuid
from django.db.models import Sum

from .utilities.model_utils import LowercaseEmailField
from .utilities.validators import validate_emails, validate_mobile_number
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)

    phone = models.CharField(
        _("Mobile Number"),
        max_length=15,
        null=True,
        blank=True,
        default=None,
        #svalidators=[validate_mobile_number],
        error_messages={"unique": "Given Mobile Number has already been registered."},
    )
    email = LowercaseEmailField(
        _("email address"),
        unique=True,
        validators=[validate_emails],
        error_messages={"unique": "Given Email has already been registered."},
    )

    username = models.CharField(max_length=255,unique=True)  
    last_name = models.CharField(max_length=255,null = True,default = '')  
    dob = models.DateField(null= True,blank= True ) 

    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200,null=True,default = '')

    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
 
    image = models.ImageField(upload_to="profiles/images",default=None,null=True,blank=True)
    role = models.PositiveSmallIntegerField(choices=roles_data, blank=True, null=True,default = 5)

    system_provider = 1
    google_provider = 2
    facebook_provider = 3

    old_password_change_case = models.BooleanField(default=True) 

    provider_CHOICES = (
        (system_provider, 'system'),
        (google_provider, 'google'),
        (facebook_provider, 'facebook'), 
        (4, 'apple'), 

    )
    provider = models.PositiveSmallIntegerField(choices=provider_CHOICES,default = system_provider)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def getRoleName(self):
        if self.role==roles.SUPER_ADMIN:
            return roles_data_dict[roles.SUPER_ADMIN]
        elif self.role == roles.ADMIN:
            return roles_data_dict[roles.ADMIN]
        elif self.role == roles.USER:
            return roles_data_dict[roles.USER]
        else:
            return None
        
    def __str__(self):
        return self.username + " "+ str(self.getRoleName())
    
    def full_name(self):
        try:
            return self.first_name + " " + self.last_name
        except:
            return self.username
    
    @property
    def ordered_price(self):
        return self.orders.all().aggregate(total_price=Sum('total_price'))['total_price']
    
    @property
    def total_rating(self):
        return self.rating.all().count()
    
    @property
    def is_app_review(self):
        return self.apprating.all().exists()

class ShippingAddress(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    profile = models.ForeignKey(CustomUser,related_name = "shipping_address", on_delete=models.CASCADE)
    provience = models.CharField(max_length = 300)
    district = models.CharField(max_length = 300)
    address_type = models.CharField(max_length=300)
    address = models.TextField()
    contact_number = models.CharField(max_length = 50)
    email = models.EmailField(max_length=100,null = True)  
    is_default = models.BooleanField(default = False)
    location = models.CharField(max_length=100,null = True)  
    description = models.CharField(max_length=300,null = True)  

    def __str__(self):
        return str(self.profile.username) + ' '+ str(self.address_type)

