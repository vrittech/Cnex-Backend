from django.db import models

# Create your models here.
class Variation(models.Model): #color
    name = models.CharField(max_length=255,unique = True)
    description = models.CharField(max_length = 1000,null = True)

    def __str__(self):
        return self.name

class VariationOption(models.Model): #red,green
    variation = models.ForeignKey(Variation,related_name = 'options', on_delete=models.CASCADE)
    value = models.CharField(max_length=255,unique = True)
    
    def __str__(self):
        return str(self.variation.name)+":" + str(self.value)  
