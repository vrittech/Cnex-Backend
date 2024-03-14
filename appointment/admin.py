from django.contrib import admin
from .models import *
# Register your models here.s

@admin.register(Services)
class AdminServices(admin.ModelAdmin):
    list_display = ['name','price']


@admin.register(Slots)
class AdminServices(admin.ModelAdmin):
    list_display = ['time_slot','number_of_staffs']


@admin.register(Appointment)
class AdminServices(admin.ModelAdmin):
    list_display = ['user','payment_amount','payment_mode']
