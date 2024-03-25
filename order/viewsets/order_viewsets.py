from ..models import Order
from ..serializers.order_serializer import OrderReadSerializers,OrderWriteSerializers
from ..serializers.order_item_serializer import OrderItemWriteSerializers
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