from django.conf import settings
import requests
from ..models import PaymentFail
from order.models import Order

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
    order = Order.objects.filter(id = data.get('order_id'),order_status = "checkout").update(payment_status = "cod",order_status="in-progress")
    return order