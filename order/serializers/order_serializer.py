from rest_framework import serializers
from ..models import Order
from products.models import Product,ProductDetailAfterVariation
from accounts.models import CustomUser,ShippingAddress
from ..models import OrderItem
from variations.models import VariationOption

class VariationSerializer_OrderItem_OrderReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['value']

class ProductSerializer_OrderItem_OrderReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','slug','featured_image']

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
    class Meta:
        model = Order
        fields = '__all__'

class OrderWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'