from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Payment
import requests

class PaymentVerify(APIView):
    def post(self, request, *args, **kwargs):
        # Implement your payment verification logic here
        # You can access request.data to get the POST data
        print("Payment success:",request.data)
        # Example payment verification logic:
        response_payment_verify,is_verify = request.data.get('payment_status','verified')

        if is_verify ==True:
            createPayment(response_payment_verify,request.data.get('payment_type'))
            return Response({'message': 'Payment verified successfully'}, status=200)
        else:
            return Response({'message': 'Payment verification failed'}, status=400)

def payment_verify(data): #Esewa
    if data.get('payment_type') == "esewa":
        response_payment,is_verify = EsewaVerify(data)
    elif data.get('payment_type') == "khalti":
        response_payment,is_verify = KhaltiVerify(data)
    return False

def createPayment(data,payment_mode):
    payload = {
        'payment_mode':payment_mode,
        'order_id':data.get('productId'),
        'ammount':data.get('totalAmount'),
        'refrence_id':data.get('referenceId'),
        'status':"paid",
    }
    Payment.objects.create(**payload)

def EsewaVerify(data):
    verification_url = f"https://rc.esewa.com.np/mobile/transaction?txnRefId={data.get('refId')}"
    merchantId = "JB0BBQ4aD0UqIThFJwAKBgAXEUkEGQUBBAwdOgABHD4DChwUAB0R"  
    merchantSecret = "BhwIWQQADhIYSxILExMcAgFXFhcOBwAKBgAXEQ==" 

    headers = {
    'merchantId':merchantId,
    'merchantSecret':merchantSecret
    }

    response = requests.get(verification_url, headers=headers)

    if response.status == "COMPLETE":
        return response,True   
    else:
        return {},False

def KhaltiVerify():
    return False
    pass

