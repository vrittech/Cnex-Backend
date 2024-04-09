from ..models import Order
from ..serializers.order_serializer import OrderReadSerializers,OrderWriteSerializers,OrderRetrieveAdminSerializers,OrderReadSerializers_customerOrder
from ..serializers.order_item_serializer import OrderItemWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from accounts import roles
from django.db.models import Q
from ..utilities.permission import OrderViewSetsPermission
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

class OrderViewsets(viewsets.ModelViewSet):
    serializer_class = OrderReadSerializers
    permission_classes = [IsAuthenticated,OrderViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Order.objects.all()

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id','created_date']

    filterset_fields = {
        'payment_status':['exact'],
        'order_status':['exact'],
        'products__product_type':['exact'],
    }

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return OrderWriteSerializers
        elif self.action in ['retrieve']:
            return OrderRetrieveAdminSerializers
        elif self.action in ['customerOrder']:
            return OrderReadSerializers_customerOrder
        return super().get_serializer_class()

    def get_queryset(self):
        if self.request.user.role in [roles.SUPER_ADMIN,roles.ADMIN]:
            query =  super().get_queryset()
        elif self.action == "ToReceiveOrder" and self.request.user.role == roles.USER:
            print("received order ")
            query = super().get_queryset().filter(Q(order_status = "in-progress") | Q(order_status = "shipped")).filter(user = self.request.user)
        elif self.request.user.role == roles.USER:
            queury = super().get_queryset().filter(user = self.request.user)

        return query.order_by("-created_date")
   
    @action(detail=False, methods=['get'], name="ToReceiveOrder", url_path="received-order")
    def ToReceiveOrder(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="customerOrder", url_path="customer-order")
    def customerOrder(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('user').distinct('user')#.annotate(total_prices=Sum('total_price'))
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)