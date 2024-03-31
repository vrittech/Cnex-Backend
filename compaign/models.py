from django.db import models

# Create your models here.

class Banner(models.Model):
    position = models.CharField(max_length = 23,choices = (('top','Top'),('middle','Middle'),('bottom','Bottom')))
    banner  = models.ImageField(upload_to='compaign/banner',null = True,blank= True)
    url = models.URLField(null = True,blank = True)

class Faqs(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()

class PrivacyPolicy(models.Model):
    description = models.TextField()

class HelpAndSupport(models.Model):
    description = models.TextField()

class TermAndCondition(models.Model):
    description = models.TextField()



    

