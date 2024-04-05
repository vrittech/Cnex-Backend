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

    def validate(self, data):
        
        print("method: ",self.context['request'].method)
        if self.context['request'].method == "POST":
            user = data['user']
            product = data['product']
            variations = data.get('variations')
            quantity = data['quantity']

            pre_order_valid = Cart.objects.filter(product__product_type = "pre-order",user = user) #if pre order exists then delete from cart
            if pre_order_valid.exists():
                pre_order_valid.delete()

            if variations:
                existing_cart_item = Cart.objects.filter(
                    user=user,
                    product=product,
                    variations__in=variations
                )
            else:
                existing_cart_item = Cart.objects.filter(
                    user=user,
                    product=product,
                )

            if existing_cart_item.exists():
                data['existing_cart_item'] = existing_cart_item.first()  # Store existing cart item in data
                return data  # Return data for updating existing cart item

        return data  # Proceed with the creation of a new cart item
    
    def create(self, validated_data):
        existing_cart_item = validated_data.pop('existing_cart_item', None)

        if existing_cart_item:
            existing_cart_item.quantity += validated_data['quantity']
            existing_cart_item.save()
            return existing_cart_item  # Return the updated existing cart item
        return super().create(validated_data)