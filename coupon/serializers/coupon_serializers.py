from rest_framework import serializers
from ..models import Coupon

class CouponReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'