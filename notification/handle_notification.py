from account.models import CustomUser
from .models import Notification,NotificatitonMessage
from .serializer import NotificationWriteSerializer
from rest_framework import status
from . import frontend_setting
from . import mapping_notification_type
# from emailmanagement.email_sender import ESendMail
from accounts import roles
from django.db.models import Q
# Assuming you have the necessary imports
from asgiref.sync import sync_to_async
from asgiref.sync import async_to_sync
import json
import asyncio
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

#notification message format
#username,website_name,blog_title,comment_message,portal_name,user_id,portal_slug

# @database_sync_to_async
def save_notification(notification_data):
    print("save notification")
    serializer = NotificationWriteSerializer(data=notification_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer

def NotificationHandler(instance,request,method,model_name):
    notification_type = 'push'
    notification_messag_obj = NotificatitonMessage.objects.all()
    if model_name == "BlogLike":
        to_notification = [instance.blogs.user_id]
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = instance.user_id
        notification_messag_reference = notification_messag_obj.filter(type = 'blog_like').first()
        path = notification_messag_reference.path.format(blog_title=instance.blogs.title,blog_id = instance.blogs.id)#f"{frontend_setting.blog_detail.format(title=instance.blogs.title,id = instance.blogs.id)}"
        notification_message = notification_messag_reference.notification_message.format(username = instance.user.username,blog_title = instance.blogs.title)#f"{instance.user.username} liked your Blog '{instance.blogs.title}'"
        particular_message = '..'
        is_read = False
    
    elif model_name == "BlogComment":
        to_notification = [instance.blogs.user_id]
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = instance.user_id
        notification_messag_reference = notification_messag_obj.filter(type = 'blog_comment').first()
        path = notification_messag_reference.path.format(blog_title=instance.blogs.title,blog_id = instance.blogs.id)#f"{frontend_setting.blog_detail.format(title=instance.blogs.title,id = instance.blogs.id)}"
        notification_message = notification_messag_reference.notification_message.format(username = instance.user.username,blog_title = instance.blogs.title)#f"{instance.user.username} commented on your Blog '{instance.blogs.title}'"
        particular_message = '..'
        is_read = False
        group_notification = '..'

    elif model_name == "Relationship":
        to_notification = [instance.followed_to_id]
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = instance.followed_by_user_id
        notification_messag_reference = notification_messag_obj.filter(type = 'relationship').first()
        path = notification_messag_reference.path.format(username=instance.followed_by_user_id)#f"{frontend_setting.user_profile_detail.format(username = instance.followed_by_user_id)}"
        notification_message = notification_messag_reference.notification_message.format(username = instance.followed_by_user.username)#f"{instance.followed_by_user.username} followed you."
        particular_message = '..'
        is_read = False

    elif model_name == "FollowNewsChannels":
        to_notification = [instance.website.user_id]
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = instance.user.id
        notification_messag_reference = notification_messag_obj.filter(type = 'follow_newschannels').first()
        try:
            path = notification_messag_reference.path.format(username = instance.user.username, portal_slug = instance.website.portal.slug)
        except:
            path = f'/publisher/{instance.website.portal.slug}'
        notification_message = notification_messag_reference.notification_message.format(username = instance.user.username,website_name = instance.website.name)
        particular_message = '..'
        is_read = False
        group_notification = '..'


    elif method == "verified_userForBlogger": # here for if user is verified then notification
        to_notification = [instance.id]
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = instance.id
        notification_messag_reference = notification_messag_obj.filter(type = 'verified_author').first()
        path = notification_messag_reference.path.format(username=instance.user.username)
        notification_message = notification_messag_reference.notification_message.format(username = instance.user.username)#
        particular_message = '..'
        is_read = False
        group_notification = '..'
    
    elif method == "reject_userForBlogger": # here for if user is verified then notification
        to_notification = [instance.id]
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = instance.id
        notification_messag_reference = notification_messag_obj.filter(type = 'reject_author').first()
        path = notification_messag_reference.path.format(username=instance.user.username)
        notification_message = notification_messag_reference.notification_message.format(username = instance.user.username)#
        particular_message = '..'
        is_read = False
        group_notification = '..'
    
    elif method == "online_portal_create": # here for if user is verified then notification
        to_notification = list(CustomUser.objects.filter(role=roles.SYSTEM_ADMIN).values_list('id', flat=True))
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = to_notification
        notification_messag_reference = notification_messag_obj.filter(type = 'online_portal_request').first()
        path = notification_messag_reference.path.format(portal_name=instance.name)
        notification_message = notification_messag_reference.notification_message.format(portal_name = instance.name,user_email = instance.requested_by_email)#
        particular_message = '..'
        is_read = False
        group_notification = '..'
    
    elif method == "is_verification_request_sent_Notification":
        
        admin_ids = list(CustomUser.objects.filter(Q(role=roles.ADMIN) | Q(role = roles.SYSTEM_ADMIN)).values_list('id', flat=True))
        to_notification = admin_ids
        # to_notification = to_notification.values_list('id',flat=True)
        from_notification = instance.id
        notification_messag_reference = notification_messag_obj.filter(type = 'is_verification_request_sent').first()
        path = notification_messag_reference.path.format(username=instance.name,user_id =instance.id)
        notification_message = notification_messag_reference.notification_message.format(username = instance.username)
        particular_message = '..'
        is_read = False
        group_notification = '..'

    elif method == "BlogCountFive": # here for if user is verified then notification
        to_notification = [instance.user_id]
        # to_notification = to_notification.values_list('id',flat=True)
        model_type = "BlogCountFive"
        from_notification = instance.user.id
        notification_messag_reference = notification_messag_obj.filter(type = 'blog_count_five').first()
        path = notification_messag_reference.path.format(username=instance.user.username,user_id = instance.user.user_id)
        notification_message = notification_messag_reference.notification_message.format(username = instance.user.username)
        particular_message = '..'
        is_read = False
        group_notification = '..'

    elif method == 'BirthDay':
        to_notification = [instance.id]
        notification_type = "admin_push"
        from_notification = instance.id
        notification_messag_reference = notification_messag_obj.filter(type = 'birthday').first()
        path = notification_messag_reference.path.format(username=instance.username,user_id = instance.id)
        notification_message = notification_messag_reference.notification_message.format(username = instance.username)
        particular_message = notification_messag_reference.particular_message.format(username = instance.username)#'Suchana Park and team wish you a very Happy Birthday! :tada: Wishing you a day filled with joy and laughter. May this year bring you success, happiness, and memorable moments.'
        is_read = False
        group_notification = '..'

    elif method == 'Anniversary':
        to_notification = [instance.id]
        notification_type = "admin_push"
        from_notification = instance.id
        notification_messag_reference = notification_messag_obj.filter(type = 'anniversary').first()
        path = notification_messag_reference.path.format(username=instance.username,user_id = instance.id)
        notification_message = notification_messag_reference.notification_message.format(username = instance.username)
        particular_message = notification_messag_reference.particular_message.format(username = instance.username)
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
        'model_type':notification_type,
        'content_object':instance,
        'content_type':ContentType.objects.get_for_model(instance).id,
        'notification_type':notification_type,
    }
    serializer = save_notification(notification_data)
    sendWebsocketNotification(serializer.data)
    return {}

def sendWebsocketNotification(data):
    # Extract the list of user IDs from the serialized data dictionary
    user_ids = data['to_notification']
     # Iterate over each user ID in the list
    for user_id in user_ids:
        # return HttpResponse("hello how are us")
        # Construct the channel name based on the current user's ID
        channel_name = f"user_{user_id}"
        # print(channel_name ,  " receive notification channel name")
        # Define the message to be sent
        
        queryset = Notification.objects.all()

        # Serialize the queryset into a list of dictionaries
        serializer = NotificationWriteSerializer(queryset, many=True)
        serialized_data = serializer.data
        
        data = json.dumps(data)
      
        message_data = {
            "type": "chat_message",
            "payload":{
                'message':data
            }
        
        }

        # Get the channel layer and send the message to the user's channel
        channel_layer = get_channel_layer()
        print(channel_layer , " channel layer.")
        async_to_sync(channel_layer.group_send)(
                channel_name,
                message_data
               
            )
