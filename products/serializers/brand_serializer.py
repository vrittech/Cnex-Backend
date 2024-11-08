from rest_framework import serializers
from ..models import Brand

class BrandReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BrandWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'