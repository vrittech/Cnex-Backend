from rest_framework import serializers
from ..models import ShippingAddress

class ShippingAddressReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class ShippingAddressWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'