from rest_framework import serializers
from ..models import ProductHaveImages

class ProductHaveImagesReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductHaveImages
        fields = ['image']

class ProductHaveImagesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductHaveImages
        fields = ['image']
        # extra_kwargs = {
        #     'image': {'required': False}  # Make the image field optional
        # }
