
from accounts.models import CustomUser
from .models import Notification
from .serializer import NotificationWriteSerializer
from rest_framework import status
from . import frontend_setting
from . import mapping_notification_type
# from emailmanagement.email_sender import ESendMail
from accounts import roles
from django.db.models import Q
# Assuming you have the necessary imports
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

def NotificationHandler(instance,request,method):

    if method == 'service_booked':
        model_name = "ModelName"
        to_notification = [instance.id]
        from_notification = instance.id
        path = frontend_setting.get(method).path.format(username=instance.username,user_id = instance.id)
        notification_message = frontend_setting.get(method).path.format(username=instance.username,user_id = instance.id)
        particular_message = frontend_setting.get(method).path.format(username=instance.username,user_id = instance.id)
        is_read = False
        group_notification = '..'
    
    notification_data = {
        "notification_message": notification_message,
        'particular_message':particular_message,
        "path": path,
        "from_notification": from_notification,
        "model_name": model_name,
        "is_read": is_read,
        "group_notification": 'USER_ADMIN',
        "to_notification": to_notification,
        'object_id':instance.id,
        'content_object':instance,
        'content_type':ContentType.objects.get_for_model(instance).id,
        'notification_type':method,
    }
    serializer = save_notification(notification_data)
    return {}

def save_notification(notification_data):
    serializer = NotificationWriteSerializer(data=notification_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


