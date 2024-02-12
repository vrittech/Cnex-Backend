from rest_framework import serializers
from ..models import Product

class ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'