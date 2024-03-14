from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Brand)
admin.site.register(Collection)
admin.site.register(Category)

admin.site.register(ProductHaveImages)
# admin.site.register(ProductDetailAfterVariation)

class ProductHaveImagesInline(admin.TabularInline):
    model = ProductHaveImages

class ProductDetailAfterVariationsInline(admin.TabularInline):
    model = ProductDetailAfterVariation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductHaveImagesInline,ProductDetailAfterVariationsInline]
    list_display = ['name','category','price']