from ..models import Product
from ..serializers.product_serializer import ProductReadSerializers,ProductWriteSerializers
from ..utilities.importbase import *

class ProductViewsets(viewsets.ModelViewSet):
    serializer_class = ProductReadSerializers
    # permission_classes = [AdminViewSetsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Product.objects.all()
    swagger_schema_title = 'ProductViewsets API'
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductWriteSerializers
        return super().get_serializer_class()
    