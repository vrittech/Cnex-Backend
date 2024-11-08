#this function is used to decrease and increase of product/variations quantity
from products.models import Product
from order.models import Cart

def quantityManage(order_obj,increase_descrease):
    order_items = order_obj.order_items.all()
    for instance in order_items:
        
        if increase_descrease == "-":
            chanages_quantity = instance.product.quantity - instance.quantity
        else:
            chanages_quantity = instance.product.quantity + instance.quantity
        
        total_variations = list(instance.variations.all().values_list('id',flat = True))
        
        prouct_obj = instance.product
        prouduct_variation_options = prouct_obj.variations.filter(variation_options__in = total_variations)
        for product_variation_item  in prouduct_variation_options:
            if increase_descrease == "-":
                product_variation_item.quantity = product_variation_item.quantity - instance.quantity
                product_variation_item.save()
            else:
                product_variation_item.quantity = product_variation_item.quantity + instance.quantity
                product_variation_item.save()

        if chanages_quantity>0:
            prouct_obj = Product.objects.filter(id = instance.product.id).update(quantity = chanages_quantity)
        else:
            prouct_obj = Product.objects.filter(id = instance.product.id).update(quantity = 0,product_type =  "pre-order")


def quantityValidation(request):
    cart_ids = request.data.get('carts')
    for cart in cart_ids:
        cart_obj = Cart.objects.get(id = cart)
        variations = list(cart_obj.variations.values_list('id', flat=True))
        quantity = cart_obj.quantity
        product_obj = cart_obj.product
        
        if quantity>product_obj.quantity:
            return False

        total_variations = variations
        prouduct_variation_options = product_obj.variations.filter(variation_options__in = total_variations)
        for product_variation_item  in prouduct_variation_options:
            if quantity > product_variation_item.quantity:
                return False
            
        return True
            