from rest_framework import serializers
from ..models import Category

class CategoryReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fiels = '__all__'

class CategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fiels = '__all__'