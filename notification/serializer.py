from .models import Notification
from accounts.models import CustomUser
from rest_framework import serializers
from accounts import roles
# from management.models import SampleForm
from . import frontend_setting



class FromUSerNotificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'phone', 'image', ]
    

class NotificationReadSerializer(serializers.ModelSerializer):  
    from_notification = FromUSerNotificationSerializers()      
    class Meta:
        model = Notification
        fields = '__all__'
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     user_role = self.context['request'].user.role
    #     path = representation.get('path',None)
    #     notification_type = representation.get('notification_type',None)
    #     instance_id = representation.get('instance_id',None)
    #     user_message = representation.get('particular_message',None)

    #     if notification_type == "new_sample_form" and user_role == roles.USER:
    #         representation['notification_message'] = user_message
            
    #         instance_refrence_obj = 1#SampleForm.objects.get(id = instance_id)
    #         path = frontend_setting.user_my_sample + str(instance_refrence_obj.refrence_number)
    #         representation['path'] = path
        
    #     elif notification_type == "customuser_create" and user_role == roles.USER:
    #         representation['notification_message'] = user_message
    #         path = frontend_setting.my_account
    #         representation['path'] = path           
            
    #     return representation
    
class NotificationWriteSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Notification
        fields = '__all__'


 