from rest_framework import serializers
from ..models import Payment

class PaymentVerifyReadSerializers(serializers.Serializer):
    order_id = serializers.CharField()
    payment_type = serializers.CharField()
    refId = serializers.CharField(required = False)