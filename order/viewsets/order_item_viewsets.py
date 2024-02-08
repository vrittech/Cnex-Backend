from ..models import OrderItem
from ..serializers.order_item_serializer import OrderItemReadSerializers,OrderItemWriteSerializers
from ..utilities.importbase import *

class OrderItemViewsets(viewsets.ModelViewSet):
    serializer_class = OrderItemReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = OrderItem.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return OrderItemWriteSerializers
        return super().get_serializer_class()
    