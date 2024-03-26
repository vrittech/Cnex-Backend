from ..models import Order
from ..serializers.order_serializer import OrderReadSerializers,OrderWriteSerializers,OrderRetrieveAdminSerializers
from ..serializers.order_item_serializer import OrderItemWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from accounts import roles

class OrderViewsets(viewsets.ModelViewSet):
    serializer_class = OrderReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Order.objects.all()

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id','created_date']

    filterset_fields = {
        'payment_status':['exact'],
        'order_status':['exact'],
    }

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return OrderWriteSerializers
        elif self.action in ['retrieve']:
            return OrderRetrieveAdminSerializers
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.role in [roles.SUPER_ADMIN,roles.ADMIN]:
            return super().get_queryset()
        elif self.request.user.role == roles.USER:
            return super().get_queryset().filter(user = self.request.user)
    