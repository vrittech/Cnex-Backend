from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Payment,PaymentFail
from order.models import Order
import requests
from django.db.models import Q
from django.conf import settings
from ..serializers.payment_verify_serializers import PaymentVerifyReadSerializers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..utilities.permission import PaymentVerifyPermission

class PaymentVerify(APIView):
    permission_classes = [IsAuthenticated,PaymentVerifyPermission]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = PaymentVerifyReadSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_obj = Order.objects.filter(user = request.user,order_id = request.data.get('order_id'))
        if not order_obj.exists():
            PaymentsFail(payment_response,request.data)
            return Response({'message': 'order not exists'}, status=400)

        if request.data.get('payment_type') == "cod":
            VerifyOrder(request.data)
        response_payment_verify, is_verify = payment_verify(request.data)
        if is_verify:
            payment_response,is_payment = createPayment(response_payment_verify, request.data.get('payment_type'))
            if is_payment:
                return Response({'message': 'Payment verified successfully'}, status=200)
            else:
                PaymentsFail(payment_response,request.data)
                return Response({'message': payment_response}, status=400)

        else:
            PaymentsFail(response_payment_verify,request.data)
            return Response({'message': response_payment_verify}, status=400)

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
    
    payment_obj = Payment.objects.filter(Q(refrence_id = payment_detail.get('referenceId')) | Q(order_id = data.get('productId')))
    if not payment_obj.exists():
        payload = {
            'payment_mode': payment_mode,
            'order_id': data.get('productId'),
            'ammount': float(data.get('totalAmount')),
            'refrence_id': payment_detail.get('referenceId'),
            'status': "paid",
        }
        Payment.objects.create(**payload)
        return "",True

    else:
        return "user have already Payment",False

def EsewaVerify(data):
    verification_url = f"https://esewa.com.np/mobile/transaction?txnRefId={data.get('refId')}"

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

def KhaltiVerify(data):
    # Implement Khalti payment verification logic here
    return None, False  # Placeholder implementation


def PaymentsFail(response , data):
    data = {
        "payment_mode":data.get('payment_type'),
        "refrence_id":data.get('refId'),
        "order_id":data.get('order_id'),
        "server_response":response,
    }
    PaymentFail.objects.create(**data)

def VerifyOrder(data):
    Order.objects.filter(id = data.get('order_id'),order_status = "checkout").update(payment_status = "cod",order_status="in-progress")
    return True
    

