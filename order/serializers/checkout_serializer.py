from rest_framework import serializers
from ..models import Checkout

class CheckoutReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'

class CheckoutWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'