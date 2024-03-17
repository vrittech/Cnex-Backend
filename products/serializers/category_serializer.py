from rest_framework import serializers
from ..models import Category

class ParentCategoryReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class CategoryReadSerializers(serializers.ModelSerializer):
    parent = ParentCategoryReadSerializers()
    childs = ParentCategoryReadSerializers(many = True)
    class Meta:
        model = Category
        fields = '__all__' 

class CategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'