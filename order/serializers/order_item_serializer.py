from rest_framework import serializers
from ..models import OrderItem

class OrderItemReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'