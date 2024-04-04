from rest_framework import serializers
from ..models import DeliveryCharge
from django.core.exceptions import ValidationError

class DeliveryChargeReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCharge
        fields = '__all__'

class DeliveryChargeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeliveryCharge
        fields = '__all__'

    def validate(self, attrs):
        data = super().validate(attrs)
          
        # Check if there are any existing records that overlap with the current price range
        overlapping_ranges = DeliveryCharge.objects.filter(
            min_price__lt=data.get('max_price'),
            max_price__gt=data.get('min_price'),
        )

        if overlapping_ranges.exists():
            raise serializers.ValidationError("Price range overlaps with existing records.")
        
        if data.get('max_price')<=data.get('min_price'):
            raise serializers.ValidationError("max price range must be greater min price range.")

        return data