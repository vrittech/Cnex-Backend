from django.contrib import admin
from .models import *

admin.site.register(Wishlist)
# admin.site.register(Cart)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    list_display = ['user','get_total_products', 'total_price','order_status']

    def get_total_products(self, obj):
        return obj.products.all().count()  # Assuming 'products' is a related field in Order model
    get_total_products.short_description = 'Total Products'


class CartItemInline(admin.TabularInline):
    model = CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

    list_display = ['user','get_total_products']

    def get_total_products(self, obj):
        return obj.products.all().count()  # Assuming 'products' is a related field in Order model
    get_total_products.short_description = 'Total Products'