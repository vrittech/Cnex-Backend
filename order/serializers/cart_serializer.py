from rest_framework import serializers
from ..models import Cart,Wishlist
from products.models import Product
from variations.models import VariationOption

class ProductSerializers_CartReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','slug','featured_image','price','quantity','title']

    def to_representation(self, instance):
        product = super().to_representation(instance)
        user = self.context['request'].user
    
        product['wishlist_exist'] = False
        if user.is_authenticated:
            wishlist_obj = Wishlist.objects.filter(user = user,products = instance)
            if wishlist_obj.exists():
                product['wishlist_exist'] = True  
        return product
                      

class variationsOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['id','value']

class CartReadSerializers(serializers.ModelSerializer):
    product = ProductSerializers_CartReadSerializers() 
    variations = variationsOptionSerializer(many = True)
    class Meta:
        model = Cart
        fields = '__all__'
    
    def to_representation(self, instance):
        representations = super().to_representation(instance)
        variations = representations.get('variations')
        price = 0
        for var in variations:
            var['price'] = instance.product.getPriceByvariation(var.get('id'))
            price = float(var['price']) + price
        tot_price = price + float(instance.product.price) - float(instance.product.discount)
        representations['tot_price'] = tot_price
            
        return representations

class CartWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'