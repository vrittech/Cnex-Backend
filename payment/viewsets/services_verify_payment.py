from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import PaymentService
import requests

class ServicePaymentVerify(APIView):
    def post(self, request, *args, **kwargs):
        response_payment_verify, is_verify = payment_verify(request.data)
        if is_verify:
            createPayment(response_payment_verify, request.data.get('payment_type'))
            return Response({'message': 'Payment verified successfully'}, status=200)
        else:
            return Response({'message': 'Payment verification failed'}, status=400)

def payment_verify(data):
    if data.get('payment_type') == "esewa":
        return EsewaVerify(data)
    elif data.get('payment_type') == "khalti":
        return KhaltiVerify(data)
    else:
        return None, False  # Return None and False if payment type is not recognized

def createPayment(data, payment_mode):
    if payment_mode == "esewa":
        payment_detail = data.get('transactionDetails')
    payload = {
        'payment_mode': payment_mode,
        'order_id': data.get('productId'),
        'ammount': float(data.get('totalAmount')),
        'refrence_id': payment_detail.get('referenceId'),
        'status': "paid",
    }
    PaymentService.objects.create(**payload)

def EsewaVerify(data):
    verification_url = f"https://rc.esewa.com.np/mobile/transaction?txnRefId={data.get('refId')}"
    merchantId = "JB0BBQ4aD0UqIThFJwAKBgAXEUkEGQUBBAwdOgABHD4DChwUAB0R"  
    merchantSecret = "BhwIWQQADhIYSxILExMcAgFXFhcOBwAKBgAXEQ==" 

    headers = {
        'merchantId': merchantId,
        'merchantSecret': merchantSecret
    }


    response = requests.get(verification_url, headers=headers)
    response_data = response.json()[0]  # Parse JSON response
    if response_data.get('transactionDetails').get('status') == "COMPLETE":
        return response_data, True   
    else:
        return response_data, False


def KhaltiVerify(data):
    # Implement Khalti payment verification logic here
    return None, False  # Placeholder implementation
