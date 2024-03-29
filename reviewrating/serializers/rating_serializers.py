from rest_framework import serializers
from ..models import Rating
from accounts.models import CustomUser
from products.models import Product


class CustomUserReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','full_name','phone']

class ProductReadSerializers_RatingReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','name','slug','featured_image']

class RatingReadSerializers(serializers.ModelSerializer):
    user = CustomUserReadSerializers()
    product = ProductReadSerializers_RatingReadSerializers()
    class Meta:
        model = Rating
        fields = '__all__'

class RatingWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'