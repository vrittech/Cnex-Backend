from ..models import Services
from ..serializers.services_serializer import ServicesReadSerializers,ServicesWriteSerializers,ServicesRetrieveSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response

class ServicesViewsets(viewsets.ModelViewSet):
    serializer_class = ServicesReadSerializers
    # permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Services.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ServicesWriteSerializers
        elif self.action in ['retrieve']:
            return ServicesRetrieveSerializers
        elif self.action in ['list']:
            return super().get_serializer_class()
    
    # @action(detail=False, methods=['post'], name="cartBulkDelete", url_path="bulk-delete")
    # def (self, request):
    #     product_ids = request.data.get('products')
    #     cart_obj = Cart.objects.filter(user=request.user,product__in = product_ids).delete()
    #     return Response({"message": "Cart bulk deleted successfully"}, status=status.HTTP_201_CREATED)
    