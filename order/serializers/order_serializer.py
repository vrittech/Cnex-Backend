from rest_framework import serializers
from ..models import Order

class OrderReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'