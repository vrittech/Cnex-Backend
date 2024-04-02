from ..models import Brand
from ..serializers.brand_serializer import BrandReadSerializers,BrandWriteSerializers
from ..utilities.importbase import *

class BrandViewsets(viewsets.ModelViewSet):
    serializer_class = BrandReadSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminViewSetsPermission]
    pagination_class = MyPageNumberPagination
    queryset  = Brand.objects.all().order_by('created_date')
    swagger_schema_title = 'Brand API'

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return BrandWriteSerializers
        return super().get_serializer_class()
    