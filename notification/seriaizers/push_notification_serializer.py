from rest_framework import serializers
from products.models import Product

class PushNotificationSerializers(serializers.Serializer):
    type =  serializers.CharField()
    id =  serializers.IntegerField()
    message = serializers.CharField()

    def validate_id(self, value):        
        type = self.initial_data.get('type')
        if type == "product_push_notification":
            query = Product.objects.filter(id = value,is_publish = True)
        
        if not query.exists():
            raise serializers.ValidationError("product is not found.")
        return query.first()