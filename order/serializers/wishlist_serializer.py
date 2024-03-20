from rest_framework import serializers
from ..models import Wishlist
from products.models import Product,Category,Brand


class BrandReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

class ParentCategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','id']

class CategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    parent = ParentCategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers()
    class Meta:
        model = Category
        fields = ['name','parent','id']

class ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    category = CategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers()
    brand = BrandReadSerializers_WishlistReadSerializers()
    class Meta:
        model = Product
        fields =  ['name','title','slug','public_id','description','price','category','quantity','brand','discount','featured_image','product_type','average_rating','total_rating']

class WishlistReadSerializers(serializers.ModelSerializer):
    products = ProductReadSerializers_WishlistReadSerializers(many = True)
    class Meta:
        model = Wishlist
        fields = '__all__'

class WishlistWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'