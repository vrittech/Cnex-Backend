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
from ..utilities.esewa_verify import VerifyOrder,payment_verify,PaymentsFail

class PaymentVerify(APIView):
    permission_classes = [IsAuthenticated,PaymentVerifyPermission]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = PaymentVerifyReadSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_obj = Order.objects.filter(user_id = request.user.id,id = request.data.get('order_id'))
        if not order_obj.exists():
            return Response({'message': 'order not exists'}, status=400)

        if request.data.get('payment_type') == "cod":
            is_verify = VerifyOrder(request.data)
            if is_verify:
                return Response({'message': 'Payment verified successfully'}, status=200)
            return Response({'message': 'Order not found '}, status=404)
        response_payment_verify, is_verify = payment_verify(request.data)
        if is_verify:
            payment_response,is_payment = createPayment(response_payment_verify, request.data.get('payment_type'))
            if is_payment:
                return Response({'message': 'Payment verified successfully'}, status=200)
            else:
                PaymentsFail(payment_response,request.data,"product")
                return Response({'message': payment_response}, status=400)

        else:
            PaymentsFail(response_payment_verify,request.data,"product")
            return Response({'message': response_payment_verify}, status=400)

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


