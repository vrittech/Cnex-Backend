from rest_framework import serializers
from ..models import Cart
from products.models import Product
from variations.models import VariationOption

class ProductSerializers_CartReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','slug','featured_image','price','quantity']

class variationsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['id','value']

class CartReadSerializers(serializers.ModelSerializer):
    product = ProductSerializers_CartReadSerializers() 
    variations = variationsOptionSerializer(many = True)
    class Meta:
        model = Cart
        fields = '__all__'
    
    def to_representation(self, instance):
        representations = super().to_representation(instance)
        variations = representations.get('variations')
        for var in variations:
            var['price'] = instance.product.getPriceByvariation(var.get('id'))    
        return representations

class CartWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'