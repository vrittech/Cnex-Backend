from rest_framework import serializers
from ..models import Product,ProductHaveImages,ProductDetailAfterVariation,Tags
from .product_have_images_serializer import ProductHaveImagesReadSerializers
from ..models import Category,Brand,Collection
from variations.models import VariationOption

import ast

def str_to_list(data,value_to_convert):
    mutable_data = data.dict()
    value_to_convert_data = mutable_data[value_to_convert]
    if type(value_to_convert_data) == list:
        return mutable_data
    try:
        variations = ast.literal_eval(value_to_convert_data)
        mutable_data[value_to_convert] = variations
        return mutable_data
    except ValueError as e:
        raise serializers.ValidationError({f'{value_to_convert}': str(e)})

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

class Tags_ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
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
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','discount','featured_image','product_type','average_rating']

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
    tags = Tags_ProductReadSerializers(many = True)
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection','tags']

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
    
    def to_internal_value(self, data):
        if data.get('collection'):
            data = str_to_list(data,'collection')
            return super().to_internal_value(data)
        return super().to_internal_value(data)
       
    def create(self, validated_data):
        images_data = self.context['request'].FILES # Extract image data
        images_data.pop('featured_image')
        product = super().create(validated_data)
        for key,image in images_data.lists():
            ProductHaveImages.objects.create(product=product, image=image[0])

        variation_data = self.initial_data.get('variation_options')
        createProductDetailAfterVariation(variation_data,product.id,"create")

        return product

def createProductDetailAfterVariation(variation_data,product,create_update):
    return True
    processed_variation_data = [{**variation, 'product': product} for variation in variation_data]
    if processed_variation_data:
        serializers = ProductDetailAfterVariation(data=processed_variation_data, many=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()
      
    print(processed_variation_data)

    