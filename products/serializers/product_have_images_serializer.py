from rest_framework import serializers
from ..models import ProductHaveImages

class ProductHaveImagesReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductHaveImages
        fiels = '__all__'

class ProductHaveImagesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductHaveImages
        fiels = '__all__'