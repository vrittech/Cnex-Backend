from ..models import Order
from ..serializers.order_serializer import OrderReadSerializers,OrderWriteSerializers
from ..utilities.importbase import *

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
    