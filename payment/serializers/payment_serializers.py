from rest_framework import serializers
from ..models import Payment

class PaymentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'