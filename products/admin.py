from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Brand)
admin.site.register(Collection)
admin.site.register(Variation)
admin.site.register(VariationOption)
admin.site.register(VariationGroup)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductHaveImages)
admin.site.register(ProductVariation)

admin.site.register(Rating)
admin.site.register(Slots)
admin.site.register(Services)

admin.site.register(Appointment)

