from rest_framework import serializers
from ..models import Wishlist

class WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class WishlistWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'