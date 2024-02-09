from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from .roles import roles_data,roles_data_dict
from .import roles
import uuid

class CustomUser(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    phone = models.CharField(max_length=15 ,unique=True,null=True , default = '')
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=255,unique=True)  

    last_name = models.CharField(max_length=255,null = True,default = '')  
    dob = models.DateField(null= True,blank= True ) 

    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200,null=True,default = '')

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
 
    image = models.ImageField(upload_to="profiles/images",default=None,null=True,blank=True)
    role = models.PositiveSmallIntegerField(choices=roles_data, blank=True, null=True)

    system_provider = 1
    google_provider = 2
    facebook_provider = 3

    old_password_change_case = models.BooleanField(default=True) 

    provider_CHOICES = (
        (system_provider, 'system'),
        (google_provider, 'google'),
        (facebook_provider, 'facebook'), 
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
            return roles_data_dict[roles.SUPER_ADMIN]
        else:
            return None
        
    def __str__(self):
        return self.username + " "+ str(self.getRoleName())
    
    def full_name(self):
        try:
            return self.first_name + " " + self.last_name
        except:
            return self.username

class ShippingAddress(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=255, choices=[
        ('home', 'Home Address'),
        ('office', 'Office Address'),
    ])
    address = models.TextField()
    location = models.CharField(max_length = 300)
    contact_number = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.profile.username) + ' '+ str(self.address_type)

