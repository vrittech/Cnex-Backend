from rest_framework import serializers
from ..models import Product,ProductHaveImages,ProductDetailAfterVariation
from .product_have_images_serializer import ProductHaveImagesReadSerializers
from ..models import Category,Brand,Collection
from variations.models import VariationOption

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

class VariationProducts_ProductRetrieveSerializers(serializers.ModelSerializer):
    # variation_options = VariationOption_VariationProducts_ProductRetrieveSerializers()

    variation_name = serializers.SerializerMethodField()
    variation_value = serializers.SerializerMethodField()
    class Meta:
        model = ProductDetailAfterVariation
        fields = '__all__'

    def get_variation_name(self,obj):
        return obj.variation_options.variation.name
    
    def get_variation_value(self,obj):
        return obj.variation_options.value

class ProductReadSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','discount','featured_image','product_type']

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
    variations = VariationProducts_ProductRetrieveSerializers(many = True)
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection','featured_image','variations']

class ProductWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
       
    def create(self, validated_data):
        images_data = self.context['request'].FILES # Extract image data
        product = super().create(validated_data)
        for key,image in images_data.lists():
            ProductHaveImages.objects.create(product=product, image=image[0])

        variation_data = self.initial_data.get('variation_options')
        createProductDetailAfterVariation(variation_data,product,"create")

        return product

def createProductDetailAfterVariation(variation_data,product,create_update):
    # return True
    variation_data = [{**variation, 'product': product} for variation in variation_data]
    print(variation_data)

    