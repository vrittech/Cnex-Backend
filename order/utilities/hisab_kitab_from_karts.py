
from coupon.models import Coupon
from ..models import Cart
from deliverycharge.models import DeliveryCharge
from django.db.models import Sum

def CartsHisabKitab(request):
    cart_ids = request.data.get('carts')
    coupon_code = request.data.get('coupon_code')

    coupon_discount = 0
    coupon_apply = False

    message = "Cart checkout get successfully"            
        
    cart_obj = Cart.objects.filter(user=request.user,id__in = cart_ids)

    total_price = 0.00
    discount = 0.00

    details = []

    
    for cart in cart_obj:
        variations  = cart.variations.all()
        product_detail = cart.product.getDetailWithVariationList(variations)

        product_total_price = (float(product_detail.get('product_price'))+float(product_detail.get('variation_price'))) * cart.quantity
        total_price = total_price + product_total_price
        discount = discount + float(cart.product.discount)*cart.quantity
        products = {
            'products':product_detail,
            'quantity':cart.quantity,
            'product_total_price':product_total_price
        }
        details.append(products)
    

    delivery_charge_obj = DeliveryCharge.objects.filter(min_price__lte=total_price, max_price__gte=total_price)
    if delivery_charge_obj.exists():
        delivery_charge_dict = delivery_charge_obj.first().get_delivery_charge()
        delivery_charge = delivery_charge_dict.get('total_delivery_charge')
    else:
        delivery_charge_dict =   {
                'delivery_charge':0,
                'is_delivery_free':False,
                'min':0,
                'max':0,
                'total_delivery_charge':0
            }
       
        delivery_charge = delivery_charge_dict.get('total_delivery_charge')

    final_total_price = total_price-discount
    if coupon_code:
        coupon_obj = Coupon.objects.filter(code = coupon_code)
        if coupon_obj.exists() and coupon_obj.first().is_verify == True:
            coupon_apply = True
            coupon_discount = coupon_obj.first().discount
            if coupon_obj.first().discount_type == "percentage":
                coupon_discount = float(coupon_obj.first().discount)/100*float(final_total_price)

        else:
            message = "Either coupon not exists or it is expired"
    final_total_price = float(delivery_charge) + final_total_price - float(coupon_discount)

    data = {
        'total_price':final_total_price,
        'products_variations_quantity_price':total_price,
        'discount':discount,
        'quantity':cart_obj.aggregate(total_quantity = Sum('quantity'))['total_quantity'],
        'checkout':details,
        'order_type':cart_obj.first().product.product_type,
        'shipping_price':delivery_charge,
        'delivery_charge_detail':delivery_charge_dict,
        'coupon_apply':coupon_apply,
        'coupon_discount':coupon_discount,
        'message':message,
    }
    return data