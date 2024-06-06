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
    search_fields = ['id','user__email','user__phone','user__first_name']
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
        
        if self.action == "ToReceiveOrder" and self.request.user.role == roles.USER:
            query = super().get_queryset().filter(Q(order_status = "in-progress") | Q(order_status = "shipped")).filter(user = self.request.user)

        elif self.action == "getFailureOrder" and self.request.user.role in [roles.SUPER_ADMIN,roles.ADMIN]:
            query = super().get_queryset().filter(order_status = "checkout")
            return query.order_by("-order_date")
        
        elif self.action == "customerOrder":
             return super().get_queryset().order_by('user').distinct('user')#.annotate(total_prices=Sum('total_price'))
           
        
        elif self.request.user.role == roles.USER:
            query = super().get_queryset().filter(user = self.request.user)

        elif self.request.user.role in [roles.SUPER_ADMIN,roles.ADMIN]:
            if self.action == "retrieve":
                return super().get_queryset()
            
            query =  super().get_queryset()

        if self.action == "partial_update":
            return query.order_by("-order_date")
        
        
        return query.order_by("-order_date").filter(~Q(order_status = "checkout"))
   
    @action(detail=False, methods=['get'], name="ToReceiveOrder", url_path="received-order")
    def ToReceiveOrder(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="getFailureOrder", url_path="checkout")
    def getFailureOrder(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="customerOrder", url_path="customer-order")
    def customerOrder(self, request, *args, **kwargs):
       return super().list(request, *args, **kwargs)