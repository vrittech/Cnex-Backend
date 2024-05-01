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
    
    def validate(self, attrs):
        attrs =  super().validate(attrs)
        if 'discount' in attrs and 'discount_type' in attrs:
            if attrs.get('discount_type') == "percentage" and int(attrs.get('discount')) > 100:
                raise serializers.ValidationError("coupon percentage can not be greater than 100%.") 
        return attrs
