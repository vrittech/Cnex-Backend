from ..models import Order
from ..serializers.order_serializer import OrderReadSerializers,OrderWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

class OrderViewsets(viewsets.ModelViewSet):
    serializer_class = OrderReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return OrderWriteSerializers
        return super().get_serializer_class()
    
    @action(detail=False, methods=['post'], name="cart_to_order", url_path="cart-to-order")
    def cart_to_order(self, request):
        return Response({"message": "add to order sucessfully."}, status=status.HTTP_201_CREATED)
    
    
