from rest_framework.views import APIView
from rest_framework.response import Response

class PaymentVerify(APIView):
    def post(self, request, *args, **kwargs):
        # Implement your payment verification logic here
        # You can access request.data to get the POST data
        print("Payment success:",request.data)
        # Example payment verification logic:
        payment_status = request.data.get('payment_status','verified')

        if payment_status == 'verified':
            return Response({'message': 'Payment verified successfully'}, status=200)
        else:
            return Response({'message': 'Payment verification failed'}, status=400)