from django.contrib.auth.models import Group, Permission
from django.contrib import admin

from .models import CustomUser,ShippingAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # list_display = ['role',] # this display in outer list form
    exclude = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email','phone','image')}),
        ('Permissions', {'fields': ('is_active','is_verified', 'is_staff', 'is_superuser','role')}),
        # ('Social sites',{'fields':('facebook','twitter','tiktok','instagram','youtube')})
        # Add your custom fields here
    )
    pass
    # Your custom admin configurations

admin.site.register(CustomUser, UserAdmin)

# admin.site.register(CustomUser)
# admin.site.register(Permission)

# admin.site.register(ShippingAddress)
@admin.register(ShippingAddress)
class AdminShippingAddress(admin.ModelAdmin):
    list_display = ['profile','address_type','provience','district','is_default']


