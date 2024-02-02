from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from rasifal.models import Astrobix

# from django.contrib.contenttypes.fields import GenericRelation
# from notification.models import Notification


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15 ,unique=True,null=True , default = '')
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=255,unique=True)  

    last_name = models.CharField(max_length=255,null = True,default = '')  
    dob = models.DateField(null= True,blank= True ) 

    is_active = models.BooleanField(default=True)
    is_verified = models.IntegerField(choices=[(0, 'Not verified'), (1, 'Verified')], default=0) #for blog
    is_rejected = models.IntegerField(choices=[(0, 'Not Rejected'), (1, 'Rejected')], default=0)
    is_verification_request_sent = models.IntegerField(choices=[(0, 'not sent'), (1, 'sent')], default=0) #for blog
    # created_by = models.IntegerField(null=True)
    remarks = models.CharField(max_length=200,null=True,default = '')
    site_link = models.CharField(max_length=200,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
 
    image = models.ImageField(upload_to="profiles/images",default=None,null=True,blank=True)
    verification_doc = models.FileField(upload_to="profiles/verification_doc/images",default=None,null=True,blank=True)#for blog

    facebook =  models.CharField(max_length=500,null=True,blank=True,default = "")
    twitter = models.CharField(max_length=500,null=True,blank=True,default = "")
    instagram = models.CharField(max_length=500,null=True,blank=True,default = "")
    youtube = models.CharField(max_length=500,null=True,blank=True,default = "")
    tiktok = models.CharField(max_length=500,null=True,blank=True,default = "")

    astrobix = models.ForeignKey(Astrobix,related_name='user',null = True ,on_delete = models.SET_NULL)

    description = models.CharField(max_length=2000,null=True,blank=True)

    SYSTEM_ADMIN = 1
    ADMIN = 2
    PUBLISHER = 3
    ADVERTISER = 4
    USER = 5
    PANDIT = 6
    
    ROLE_CHOICES = (
        (SYSTEM_ADMIN, 'SYSTEM_ADMIN'),
        (ADMIN, 'ADMIN'),
        (PUBLISHER, 'PUBLISHER'),
        (ADVERTISER, 'ADVERTISER'),
        (USER, 'USER'),
        (PANDIT, 'PANDIT'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

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

    # notification = GenericRelation(Notification)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def getRoleName(self):
        if self.role==1:
            return 'SYSTEM_ADMIN'
        elif self.role == 2:
            return 'ADMIN'
        elif self.role == 3:
            return 'PUBLISHER'
        elif self.role == 4:
            return 'ADVERTISER'
        elif self.role == 5:
            return 'USER'
        elif self.role == 6:
            return 'PANDIT'#Umesh Baba'
        else:
            return ''
        
    def __str__(self):
        return self.username + " "+ str(self.getRoleName())
    
    def full_name(self):
        try:
            return self.first_name + " " + self.last_name
        except:
            return self.username

class Relationship(models.Model):
    followed_by_user = models.ForeignKey(CustomUser,related_name="following", on_delete=models.CASCADE)
    followed_to = models.ForeignKey(CustomUser,related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('followed_by_user','followed_to')

