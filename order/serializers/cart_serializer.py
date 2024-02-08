from rest_framework import serializers
from ..models import Cart

class CartReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'