from ..models import Category
from ..serializers.category_serializer import CategoryReadSerializers,CategoryWriteSerializers
from ..utilities.importbase import *

class CategoryViewsets(viewsets.ModelViewSet):
    serializer_class = CategoryReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Category.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CategoryWriteSerializers
        return super().get_serializer_class()
    