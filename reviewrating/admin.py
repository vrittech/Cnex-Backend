from django.contrib import admin
from .models import  Rating,AppRating
# Register your models here.
admin.site.register([Rating,AppRating])
