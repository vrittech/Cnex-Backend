from django.db import models

# Create your models here.

class Banner(models.Model):
    position = models.CharField(max_length = 23,choices = (('top','Top'),('middle','Middle'),('bottom','Bottom')))
    banner  = models.ImageField(upload_to='compaign/banner')
    url = models.URLField()

class Faqs(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()

class PrivacyPolicy(models.Model):
    description = models.TextField()



    

