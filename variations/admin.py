from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(Variation)

@admin.register(VariationOption)
class AdminVariationOption(admin.ModelAdmin):
    list_display = ['variation','value']

@admin.register(VariationGroup)
class AdminVariationGroup(admin.ModelAdmin):
    list_display = ['id','name']

class VariationOptionInline(admin.TabularInline):
    model = VariationOption

@admin.register(Variation)
class AdminVariation(admin.ModelAdmin):
    inlines = [VariationOptionInline]
    list_display = ['name']