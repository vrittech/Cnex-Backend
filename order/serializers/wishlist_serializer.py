from rest_framework import serializers
from ..models import Wishlist
from products.models import Product

class ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class WishlistReadSerializers(serializers.ModelSerializer):
    products = ProductReadSerializers_WishlistReadSerializers(many = True)
    class Meta:
        model = Wishlist
        fields = '__all__'

class WishlistWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'