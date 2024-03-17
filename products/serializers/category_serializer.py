from rest_framework import serializers
from ..models import Category
import json
import ast

def str_to_list(data,variations):
    mutable_data = data.dict()
    variations = mutable_data['variations']
    if type(variations) == list:
        return mutable_data
    try:
        variations = ast.literal_eval(variations)
        mutable_data['variations'] = variations
        return mutable_data
    except ValueError as e:
        raise serializers.ValidationError({'variations': str(e)})
  
class ParentCategoryReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

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
    
    def to_internal_value(self, data):
        if data.get('variations'):
            data = str_to_list(data,'variations')
            return super().to_internal_value(data)
        return super().to_internal_value(data)