from rest_framework import serializers
from ..models import Product,ProductHaveImages,ProductDetailAfterVariation,Tags
from .product_have_images_serializer import ProductHaveImagesReadSerializers
from .product_details_after_variation_serializer import ProductDetailAfterVariationWriteSerializers
from ..models import Category,Brand,Collection
from variations.models import VariationOption,Variation
from order.models import Wishlist,Cart

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

class VariationAdmin_ProductRetrieveAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['id','name']    

class VariationOptionRetrieveAdmin_VariationProducts_ProductRetrieveAdminSerializers(serializers.ModelSerializer):
    variation = VariationAdmin_ProductRetrieveAdminSerializers()
    class Meta:
        model = VariationOption
        fields = ['variation','id','value']

class CategoryReadSerializers_CategoryReadSerializers_ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','id']

class CategoryReadSerializers_ProductReadSerializers(serializers.ModelSerializer):
    parent = CategoryReadSerializers_CategoryReadSerializers_ProductReadSerializers()
    class Meta:
        model = Category
        fields = ['name','parent','id']

class BrandReadSerializers_ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

class CollectionSerializers_ProductReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['name','id']

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
    

class VariationProducts_ProductRetrieveAdminSerializers(serializers.ModelSerializer):
    # variation_options = VariationOptionRetrieveAdmin_VariationProducts_ProductRetrieveAdminSerializers()

    # variation_name = serializers.SerializerMethodField()
    # variation_value = serializers.SerializerMethodField()
    class Meta:
        model = ProductDetailAfterVariation
        fields =  []
    
    def to_representation(self, instance):
        representations = super().to_representation(instance)
        price = instance.price
        quantity = instance.quantity
        variation = instance.variation_options

        representations['variation']=variation.variation.name
        representations['variation_id']=variation.variation.id
        representations['variation_option_value']=variation.value
        representations['variation_value_id']=variation.id
        representations['price'] = price
        representations['quantity'] = quantity
    
        return representations

    def get_variation_name(self,obj):
        return obj.variation_options.variation.name
    
    def get_variation_value(self,obj):
        return obj.variation_options.value
    

class VariationProducts_ProductReadAdminSerializers(serializers.ModelSerializer):
    # variation_options = VariationOption_VariationProducts_ProductRetrieveSerializers()

    variation_name = serializers.SerializerMethodField()
    variation_value = serializers.SerializerMethodField()
    class Meta:
        model = ProductDetailAfterVariation
        fields = ['variation_name','variation_value']

    def get_variation_name(self,obj):
        return obj.variation_options.variation.name
    
    def get_variation_value(self,obj):
        return obj.variation_options.value

class ProductReadSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    # variations = VariationProducts_ProductRetrieveSerializers(many = True)
    collection = CollectionSerializers_ProductReadSerializers(many = True)
    class Meta:
        model = Product
        fields = ['has_variations','id','name','title','slug','public_id','description','price','category','quantity','brand','product_images','discount','featured_image','product_type','average_rating','total_rating','collection']
    
    def to_representation(self, instance):
        product = super().to_representation(instance)
        user = self.context['request'].user
    
        product['wishlist_exists'] = False
        product['cart_exist'] = True   
        if user.is_authenticated:
            wishlist_obj = Wishlist.objects.filter(user = user,products = instance)
            cart_obj = Cart.objects.filter(user = user,products = instance)
            if wishlist_obj.exists():
                product['wishlist_exist'] = True  
            if cart_obj.exists():
                product['cart_exist'] = True                            

        return product

class ProductReadAdminSerializers(serializers.ModelSerializer):
    # product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    variations = VariationProducts_ProductReadAdminSerializers(many = True)
    class Meta:
        model = Product
        fields = ['id','name','title','slug','public_id','description','price','category','quantity','brand','discount','product_type','featured_image','variations','total_variations_quantity','is_stock']

class ProductRetrieveAdminSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    collection = CollectionSerializers_ProductReadSerializers(many = True)
    tags = Tags_ProductReadSerializers(many = True)
    variations = VariationProducts_ProductRetrieveAdminSerializers(many = True)
    class Meta:
        model = Product
        fields = ['name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection','tags','discount','product_type','featured_image','is_best_sell','is_manage_stock','is_publish','variations']

class ProductRetrieveSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    collection = CollectionSerializers_ProductReadSerializers(many = True)
    variations = VariationProducts_ProductRetrieveSerializers(many = True)
    class Meta:
        model = Product
        fields = ['id','name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection','featured_image','variations','product_type','discount','average_rating','total_rating']
    
    def to_representation(self, instance):
        product = super().to_representation(instance)
        user = self.context['request'].user
    
        product['wishlist_exists'] = False
        if user.is_authenticated:
            wishlist_obj = Wishlist.objects.filter(user = user,products = instance)
            if wishlist_obj.exists():
                product['wishlist_exist'] = True                            

        return product

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
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
              

def createProductDetailAfterVariation(variation_data,product,create_update):
    variation_data = ast.literal_eval(variation_data)
    processed_variation_data = [{**variation,'variation_options':variation.get('id') ,'product': product} for variation in variation_data]
    if processed_variation_data:
        serializers = ProductDetailAfterVariationWriteSerializers(data=processed_variation_data, many=True)
        serializers.is_valid(raise_exception=True)
        serializers.save()

    # [{"id":13,"name":"red","quantity":"1","price":"20"},{"id":14,"name":"steel","quantity":"1","price":"20"},{"id":15,"name":"copper","quantity":"2","price":"34"}]