from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Variation)
admin.site.register(VariationOption)
admin.site.register(VariationGroup)