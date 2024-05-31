from rest_framework import serializers
from ..models import Product,ProductHaveImages,ProductDetailAfterVariation,Tags
from .product_have_images_serializer import ProductHaveImagesReadSerializers
from .product_details_after_variation_serializer import ProductDetailAfterVariationWriteSerializers
from ..models import Category,Brand,Collection
from variations.models import VariationOption,Variation
from order.models import Wishlist,Cart
from ..utilities.variations_group import ArrangeVariationGroup
from django.db import transaction
from notification.models import Notification

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
        fields = ['name','slug','id']

class CategoryReadSerializers_ProductReadSerializers(serializers.ModelSerializer):
    parent = CategoryReadSerializers_CategoryReadSerializers_ProductReadSerializers()
    class Meta:
        model = Category
        fields = ['name','slug','parent','id']

class CategoryReadSerializers_ProductRetrieveAdminSerializers(serializers.ModelSerializer):
    childs = CategoryReadSerializers_CategoryReadSerializers_ProductReadSerializers(many = True)
    parent = CategoryReadSerializers_CategoryReadSerializers_ProductReadSerializers()
    class Meta:
        model = Category
        fields = ['name','slug','id','childs','parent']

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
        representations['id']=instance.id
    
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
        fields = ['variation_name','variation_value','quantity']

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
        fields = ['has_variations','id','name','title','slug','public_id','description','price','category','quantity','brand','product_images','discount','featured_image','product_type','average_rating','total_rating','collection','is_stock']
    
    def to_representation(self, instance):
        product = super().to_representation(instance)
        user = self.context['request'].user
    
        product['wishlist_exists'] = False
        if user.is_authenticated:
            wishlist_obj = Wishlist.objects.filter(user = user,products = instance)
            if wishlist_obj.exists():
                product['wishlist_exists'] = True  
           
        return product

class ProductReadAdminSerializers(serializers.ModelSerializer):
    # product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    variations = VariationProducts_ProductReadAdminSerializers(many = True)
    notification = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['notification','is_stock','is_publish','initial_quantity','id','name','title','slug','public_id','description','price','category','quantity','brand','discount','product_type','featured_image','variations','total_variations_quantity','is_stock']

    def get_notification(self,obj):
        notify_obj = Notification.objects.filter(notification_type = "product_push_notification",object_id = obj.id)
        if notify_obj.exists():
            return {"count":notify_obj.count(),'last_notify':notify_obj.last().created_date}
        else:
            return {"count":notify_obj.count(),'last_notify':""}
    

class ProductRetrieveAdminSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductRetrieveAdminSerializers()
    collection = CollectionSerializers_ProductReadSerializers(many = True)
    tags = Tags_ProductReadSerializers(many = True)
    variations = VariationProducts_ProductRetrieveAdminSerializers(many = True)
    class Meta:
        model = Product
        fields = ['is_stock','name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection','tags','discount','product_type','featured_image','is_best_sell','is_manage_stock','is_publish','variations']
    
    def to_representation(self, instance):
        representations  = super().to_representation(instance)
        variations = representations.get('variations')
        representations['variations_group'] = ArrangeVariationGroup(variations)
    
        return representations

class ProductRetrieveSerializers(serializers.ModelSerializer):
    product_images = ProductHaveImagesReadSerializers(many = True)
    brand = BrandReadSerializers_ProductReadSerializers()
    category = CategoryReadSerializers_ProductReadSerializers()
    collection = CollectionSerializers_ProductReadSerializers(many = True)
    variations = VariationProducts_ProductRetrieveSerializers(many = True)
    class Meta:
        model = Product
        fields = ['total_sale','is_stock','id','name','title','slug','public_id','description','price','category','quantity','brand','product_images','collection','featured_image','variations','product_type','discount','average_rating','total_rating']
    
    def to_representation(self, instance):
        product = super().to_representation(instance)
        user = self.context['request'].user
    
        product['wishlist_exists'] = False
        product['is_rate'] = False

        if user.is_authenticated:
            wishlist_obj = Wishlist.objects.filter(user = user,products = instance)
            if wishlist_obj.exists():
                product['wishlist_exist'] = True   

            rate_obj = user.rating.all().filter(product = instance)
            if rate_obj.exists():
                product['is_rate'] = True  
                # product['rate_id'] = rate_obj.first().id                            

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
    
    @transaction.atomic
    def create(self, validated_data):
        images_data = self.context['request'].FILES # Extract image data
        try:
            images_data.pop('featured_image')
        except:
            pass
     
        product = super().create(validated_data)
        for key,image in images_data.lists():
            ProductHaveImages.objects.create(product=product, image=image[0])

        variation_data = self.initial_data.get('variation_options')
        createProductDetailAfterVariation(variation_data,product.id,"create")

        return product
    
    @transaction.atomic
    def update(self, instance, validated_data):
        images_data = self.context['request'].FILES # Extract image data
        try:
            images_data.pop('featured_image')
        except:
            pass
        updated_instance = super().update(instance, validated_data)

        for key,image in images_data.lists():
            ProductHaveImages.objects.create(product=updated_instance, image=image[0])

        variation_data = self.initial_data.get('variation_options')
        if variation_data:
            createProductDetailAfterVariation(variation_data,updated_instance.id,"update")

        return updated_instance
              

def createProductDetailAfterVariation(variation_data,product,create_update):
    if create_update == "create":
        variation_data = ast.literal_eval(variation_data)
        processed_variation_data = [{**variation,'variation_options':variation.get('id') ,'product': product} for variation in variation_data]
        if processed_variation_data:
            serializers = ProductDetailAfterVariationWriteSerializers(data=processed_variation_data, many=True)
            serializers.is_valid(raise_exception=True)
            serializers.save()
    elif create_update == "update":
        variation_data = ast.literal_eval(variation_data)

        ProductDetailAfterVariation_objs_list =  list(ProductDetailAfterVariation.objects.filter(product_id = product).values_list('variation_options_id',flat=True))
        print(ProductDetailAfterVariation_objs_list)
        
        ProductDetailAfterVariation.objects.filter(product_id = product).delete() #this let variation delete from product. this is not best method. please use another best 
        
        for variation in variation_data:

            try:
                ProductDetailAfterVariation_objs_list.remove(variation.get('id'))
            except:
                print("can't remove , element not found.")

            create_payload = {**variation,'variation_options':variation.get('id') ,'product': product} 
            product_have_variation_obj = ProductDetailAfterVariation.objects.filter(product_id = product,variation_options = variation.get('id'))
            if product_have_variation_obj.exists():
                product_have_variation_obj = product_have_variation_obj.first()
            else:
                product_have_variation_obj = None
            
            serializers = ProductDetailAfterVariationWriteSerializers(product_have_variation_obj,data=create_payload, partial=True)
            serializers.is_valid(raise_exception=True)
            serializers.save()
        
        print(variation_data,"remaining id ", ProductDetailAfterVariation_objs_list)
        deleted_cart_obj = Cart.objects.filter(variations__in = ProductDetailAfterVariation_objs_list)
        print("deleted cart ",deleted_cart_obj)
        deleted_cart_obj.delete()
    
    
               
    # [{"id":13,"name":"red","quantity":"1","price":"20"},{"id":14,"name":"steel","quantity":"1","price":"20"},{"id":15,"name":"copper","quantity":"2","price":"34"}]