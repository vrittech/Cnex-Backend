
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
from .mapping_notification_type import mapping

def NotificationHandler(instance,method,request = None):

    if method == 'password_changed':
        to_notification = [instance.id]
        from_notification = instance.id
        path = "#"
        notification_message = mapping.get(method).get('admin_message').format(username=instance.username,user_id = instance.id)
        user_messaage = mapping.get(method).get('user_message').format(username=instance.username,user_id = instance.id)
        is_read = False
        group_notification = '..'

    if method == 'payment_confirmed':
        to_notification = [instance.user.id]
        from_notification = instance.user.id
        path = mapping.get(method).get('path').format(order_id=instance.id)
        notification_message = mapping.get(method).get('admin_message').format(order_id=instance.id)
        user_messaage = mapping.get(method).get('user_message').format(username=instance.username,user_id = instance.id)
        is_read = False
        group_notification = '..'
    
    if method == 'service_booked':
        services = instance.checkout_appointment.services_items.all()
        services_names = ','.join([service.service.name for service in services])
        to_notification = [instance.user.id]
        from_notification = instance.user.id
        path = mapping.get(method).get('path').format(order_id=instance.id)
        notification_message = mapping.get(method).get('admin_message').format(services_name=services_names)
        user_messaage = mapping.get(method).get('admin_message').format(services_name=services_names)
        is_read = False
        group_notification = '..'

    if method == 'order_shipped':
        to_notification = [instance.user.id]
        from_notification = instance.user.id
        path = mapping.get(method).get('path').format(order_id=instance.id)
        notification_message = mapping.get(method).get('admin_message').format(order_id=instance.id)
        user_messaage = mapping.get(method).get('user_message').format(username=instance.username,user_id = instance.id)
        is_read = False
        group_notification = '..'

    if method == 'order_delivered':
        to_notification = [instance.user.id]
        from_notification = instance.user.id
        path = mapping.get(method).get('path').format(order_id=instance.id)
        notification_message = mapping.get(method).get('admin_message').format(order_id=instance.id)
        user_messaage = mapping.get(method).get('user_message').format(username=instance.username,user_id = instance.id)
        is_read = False
        group_notification = '..'

    if method == 'order_cancelled':
        to_notification = [instance.user.id]
        from_notification = instance.user.id
        path = mapping.get(method).get('path').format(order_id=instance.id)
        notification_message = mapping.get(method).get('admin_message').format(order_id=instance.id)
        user_messaage = mapping.get(method).get('user_message').format(username=instance.username,user_id = instance.id)
        is_read = False
        group_notification = '..'

    notification_data = {
        "notification_message": notification_message,
        "path": path,
        "from_notification": from_notification,
        "is_read": is_read,
        "group_notification": 'USER_ADMIN',
        "to_notification": to_notification,
        'object_id':instance.id,
        'content_object':instance,
        'content_type':ContentType.objects.get_for_model(instance).id,
        'notification_type':method,
    }
    serializer = save_notification(notification_data)
    sendNotificationToOneSignals(notification_data)
    return True

def save_notification(notification_data):
    serializer = NotificationWriteSerializer(data=notification_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


