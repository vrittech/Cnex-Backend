from ..models import ProductHaveImages
from ..serializers.product_have_images_serializer import ProductHaveImagesReadSerializers,ProductHaveImagesWriteSerializers
from ..utilities.importbase import *

class ProductHaveImagesViewsets(viewsets.ModelViewSet):
    serializer_class = ProductHaveImagesReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = ProductHaveImages.objects.all()
    swagger_schema_title = 'ProductHaveImagesViewsets API'
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductHaveImagesWriteSerializers
        return super().get_serializer_class()
    