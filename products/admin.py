from django.contrib import admin
from .models import *


admin.site.register([Category,Collection,Brand,Tags])

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