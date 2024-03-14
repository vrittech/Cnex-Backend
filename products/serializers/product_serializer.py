from rest_framework import serializers
from ..models import Product
from .product_have_images_serializer import ProductHaveImagesWriteSerializers

class ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductWriteSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesWriteSerializers(many = True)
    class Meta:
        model = Product
        fields = '__all__'