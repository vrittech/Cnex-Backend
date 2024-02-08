from ..models import ProductDetailAfterVariation
from ..serializers.product_details_after_variation_serializer import  ProductDetailAfterVariationReadSerializers,ProductDetailAfterVariationWriteSerializers
from ..utilities.importbase import *

class ProductDetailAfterVariationViewsets(viewsets.ModelViewSet):
    serializer_class = ProductDetailAfterVariationReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = ProductDetailAfterVariation.objects.all()
    swagger_schema_title = 'ProductDetailAfterVariationViewsets API'
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductDetailAfterVariationWriteSerializers
        return super().get_serializer_class()