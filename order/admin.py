from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Order)
# admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Cart)

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['public_id', 'order', 'product_variation', 'quantity']

class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    list_display = ['user','get_total_products', 'total_price','order_status']

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.prefetch_related('products')  # Assuming 'products' is a related field in Order model
    #     return queryset

    def get_total_products(self, obj):
        return obj.products.all().count()  # Assuming 'products' is a related field in Order model
    get_total_products.short_description = 'Total Products'