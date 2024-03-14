from rest_framework import serializers
from ..models import Product,ProductHaveImages
from .product_have_images_serializer import ProductHaveImagesWriteSerializers

class ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductWriteSerializers(serializers.ModelSerializer):
    # product_images = ProductHaveImagesWriteSerializers(many = True)
    class Meta:
        model = Product
        fields = '__all__'
       
    def create(self, validated_data):
        images_data = self.context['request'].FILES # Extract image data
        product = super().create(validated_data)
        for key,image in images_data.lists():
            ProductHaveImages.objects.create(product=product, image=image[0])
        return product
