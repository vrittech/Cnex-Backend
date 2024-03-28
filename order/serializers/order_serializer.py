from rest_framework import serializers
from ..models import Order
from products.models import Product,ProductDetailAfterVariation
from accounts.models import CustomUser,ShippingAddress
from ..models import OrderItem
from variations.models import VariationOption
from coupon.models import Coupon

class VariationSerializer_OrderItem_OrderReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['value']

class ProductSerializer_OrderItem_OrderReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','slug','featured_image','product_type']

class CustomUserSerializers_OrderReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','username','first_name','last_name','phone']

class ShippingAddressSerializers_OrderReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address_type','address','location','contact_number']

class OrderItem_OrderReadSerializers(serializers.ModelSerializer):
    product = ProductSerializer_OrderItem_OrderReadSerializers()
    variations = VariationSerializer_OrderItem_OrderReadSerializers(many = True)
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItem_OrderRetrieveAdminSerializers(serializers.ModelSerializer):
    product = ProductSerializer_OrderItem_OrderReadSerializers()
    variations = VariationSerializer_OrderItem_OrderReadSerializers(many = True)
    unit_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = '__all__'
     
    def get_unit_price(self,obj):
        return 20
    
    def get_total_price(self,obj):
        return 2323
    
class CouponSerializer_OrderRetrieveAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class OrderReadSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers_OrderReadSerializers()
    order_items = OrderItem_OrderReadSerializers(many = True)
    delivery_address = ShippingAddressSerializers_OrderReadSerializers()
    class Meta:
        model = Order
        fields = ['id','quantity','total_price','quantity','payment_status','order_status','order_date','coupons','delivery_address','user','order_items']

class OrderReadAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderRetrieveAdminSerializers(serializers.ModelSerializer):
    user = CustomUserSerializers_OrderReadSerializers()
    order_items = OrderItem_OrderRetrieveAdminSerializers(many = True)
    delivery_address = ShippingAddressSerializers_OrderReadSerializers()
    coupons = CouponSerializer_OrderRetrieveAdminSerializers()
    class Meta:
        model = Order
        # fields = '__all__'
        exclude  = ['products']

class OrderWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class BuyNowOrderWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        order_items = self.context['request'].data.get('variations')
        print(order_items, "::order items ")
        return instance