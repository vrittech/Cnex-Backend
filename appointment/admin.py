from django.contrib import admin
from .models import *
# Register your models here.s

admin.site.register(Slots)

class AdminSlotsInline(admin.TabularInline):
    model = Slots

@admin.register(Services)
class AdminServices(admin.ModelAdmin):
    inlines = [AdminSlotsInline]
    list_display = ['name','price']

@admin.register(Appointment)
class AdminServices(admin.ModelAdmin):
    list_display = ['user','payment_amount','payment_mode']
