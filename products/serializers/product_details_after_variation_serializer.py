from rest_framework import serializers
from ..models import ProductDetailAfterVariation

class ProductDetailAfterVariationReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductDetailAfterVariation
        fields = '__all__'

class ProductDetailAfterVariationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductDetailAfterVariation
        fields = '__all__'
    
    def validate_quantity(self,value):
        if value > self.instance.product.quantity:
            raise serializers.ValidationError("Quantity cannot exceed available stock.")
        return value
