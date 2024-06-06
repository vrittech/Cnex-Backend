from django.conf import settings
import requests
from ..models import PaymentFail
from order.models import Order
from products.models import Product

def payment_verify(data):
    if data.get('payment_type') == "esewa":
        return EsewaVerify(data)
    else:
        return None, False  # Return None and False if payment type is not recognized

def EsewaVerify(data):
    verification_url = f"https://esewa.com.np/mobile/transaction?txnRefId={data.get('refId')}"
    # verification_url = f"https://rc.esewa.com.np/mobile/transaction?txnRefId={data.get('refId')}"
    headers = {
        'merchantId': settings.ESEWA_MERCHANT_ID,
        'merchantSecret': settings.ESEWA_MERCHANT_SECRETE
    }

    response = requests.get(verification_url, headers=headers)
    try:
        response_data = response.json()[0] # Parse JSON response
    except:
        return response.json(),False
    
    if response_data.get('transactionDetails').get('status') == "COMPLETE":
        if response_data.get('productId') != data.get('order_id'):
            return "Order id not match",False
        return response_data, True   
    else:
        return response_data, False
    

def PaymentsFail(response , data , service_product):
    data = {
        "payment_mode":data.get('payment_type'),
        "refrence_id":data.get('refId'),
        "order_id":data.get('order_id'),
        "server_response":response,
        "services_product":service_product,
    }
    PaymentFail.objects.create(**data)


def VerifyOrder(data):#for cod products
    order_obj = Order.objects.filter(id = data.get('order_id'),order_status = "checkout")

    order_items = order_obj.first().order_items.all()
    for instance in order_items:
        chanages_quantity = instance.product.quantity - instance.quantity
        if chanages_quantity>0:
            prouct_obj =Product.objects.filter(id = instance.product.id).update(quantity = chanages_quantity)
            total_variations = list(instance.variations.all().value_list('variations',flat = True))
            prouduct_variation_options = prouct_obj.first().variations.filter(variation_options__in = total_variations)
            for product_variation_item  in prouduct_variation_options:
                product_variation_item.update(quantity =product_variation_item.quantity - instance.quantity)
        else:
            prouct_obj = Product.objects.filter(id = instance.product.id).update(quantity = 0,product_type =  "pre-order")

    return order_obj.update(payment_status = "cod",order_status="in-progress")