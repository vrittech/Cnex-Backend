from rest_framework import serializers
from ..models import Collection
from notification.models import Notification

class CollectionReadSerializers(serializers.ModelSerializer):
    notification = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = '__all__'
    
    def get_notification(self,obj):
        notify_obj = Notification.objects.filter(notification_type = "collection_push_notification",object_id = obj.id)
        if notify_obj.exists():
            return {"count":notify_obj.count(),'last_notify':notify_obj.last().created_date}
        else:
            return {"count":notify_obj.count(),'last_notify':""}

class CollectionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'