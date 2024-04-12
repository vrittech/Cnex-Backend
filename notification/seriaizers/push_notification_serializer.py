from rest_framework import serializers
from products.models import Collection,Product

class PushNotificationSerializers(serializers.Serializer):#for instance
    type =  serializers.CharField()
    title = serializers.CharField()
    id =  serializers.IntegerField()
    url =  serializers.URLField(required = False)
    message = serializers.CharField()
    file = serializers.FileField(required = False)

    def validate_id(self, value):        
        type = self.initial_data.get('type')
        if type == "product_push_notification":
            query = Product.objects.filter(id = value,is_publish = True)
        elif type == "collection_push_notification":
            query = Collection.objects.filter(id = value)
        else:
            query = Product.objects.none()
        if not query.exists():
            raise serializers.ValidationError("product is not found.")
        return query.first()
    

class PushNotificationSerializers_without_id(serializers.Serializer):#for not instance
    type =  serializers.CharField()
    title = serializers.CharField()
    message = serializers.CharField()
    file = serializers.FileField(required = False)
    url =  serializers.URLField(required = False)
    path =  serializers.CharField(required = False)