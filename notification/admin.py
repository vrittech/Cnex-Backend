from django.contrib import admin
from .models import Notification

# Register your models here.

# admin.site.register(Notification)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display=['notification_message','id']
