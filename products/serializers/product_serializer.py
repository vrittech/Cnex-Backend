from rest_framework import serializers
from ..models import Product,ProductHaveImages
from .product_have_images_serializer import ProductHaveImagesReadSerializers
from ..models import Category,Brand,Collection

class CategoryReadSerializers_ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class BrandReadSerializers_ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

class CollectionSerializers_ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['name']

class ProductReadSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images']

class ProductReadAdminSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','discount','product_type']

class ProductRetrieveAdminSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    collection = CollectionSerializers_ProductReadSerializers()
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection']

class ProductRetrieveSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    collection = CollectionSerializers_ProductReadSerializers()
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection']

class ProductWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
       
    def create(self, validated_data):
        images_data = self.context['request'].FILES # Extract image data
        product = super().create(validated_data)
        for key,image in images_data.lists():
            ProductHaveImages.objects.create(product=product, image=image[0])
        return product
