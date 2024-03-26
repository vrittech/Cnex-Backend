from rest_framework import serializers
from ..models import DeliveryCharge

class DeliveryChargeReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCharge
        fields = '__all__'

class DeliveryChargeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCharge
        fields = '__all__'