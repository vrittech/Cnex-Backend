from ..models import Order
from ..serializers.order_serializer import OrderWriteSerializers
from ..serializers.order_item_serializer import OrderItemWriteSerializers
from ..models import Cart
from django.db import transaction
from ..utilities.hisab_kitab_from_karts import CartsHisabKitab

@transaction.atomic
def CartToOrder(request,carts,coupon_obj = None):
    hisab_kitab_data = CartsHisabKitab(request)
    order_payload = {
        'user':request.user.id,
        'delivery_address':request.data.get('shipping_id'),
        'quantity':hisab_kitab_data.get('quantity'),
        'sub_total_price':hisab_kitab_data.get('products_variations_quantity_price'),
        'total_price':hisab_kitab_data.get('total_price'),
        'coupon_discount':hisab_kitab_data.get('coupon_discount'),
        'total_discount':hisab_kitab_data.get('discount'),
        'order_status':'checkout',
        'shipping_price':hisab_kitab_data.get('shipping_price'),
        'is_delivery_free':hisab_kitab_data.get('delivery_charge_detail').get('is_delivery_free'),
        'payment_status':'unpaid',
        'order_type':hisab_kitab_data.get('order_type')
    }
    if coupon_obj != None:
        order_payload['coupons'] = coupon_obj.first().id

    order_serializer = OrderWriteSerializers(data = order_payload)
    order_serializer.is_valid(raise_exception=True)
    order_serializer.save()

    order_items = []

    for cart in carts:
        cart_obj = Cart.objects.get(id = cart)
        variations = list(cart_obj.variations.values_list('id', flat=True))

        if len(variations)>0:
            total_variations_price = cart_obj.product.getvariationPriceOnly(variations)
        else:
            total_variations_price = 0

        items_payload = {
            'order':order_serializer.data.get('id'),
            'product':cart_obj.product.id,
            'quantity':cart_obj.quantity,
            'price':cart_obj.product.price,
            'discount':cart_obj.product.discount,
            'price_with_variation':float(cart_obj.product.price) + total_variations_price,
            'total_price':float(cart_obj.product.price)*float(cart_obj.quantity)+float(total_variations_price)-float(cart_obj.product.discount)
        }

        if len(variations)>0:
            items_payload['variations'] = variations
            items_payload['variations_price']=cart_obj.product.getvariationPriceOnly(variations)
        else:
            total_variations_price = 0
        
        
        order_items.append(items_payload)
    
    order_items_serializers = OrderItemWriteSerializers(data = order_items,many = True)
    order_items_serializers.is_valid(raise_exception=True)
    order_items_serializers.save()

    Cart.objects.filter(id__in = carts,user = request.user).delete()

    return order_serializer.data.get('id')
    