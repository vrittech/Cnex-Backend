from ..models import Category
from ..serializers.category_serializer import CategoryReadSerializers,CategoryWriteSerializers
from ..utilities.importbase import *

class CategoryViewsets(viewsets.ModelViewSet):
    serializer_class = CategoryReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Category.objects.all().order_by('order_at')
    lookup_field = 'slug'

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name','slug']
    ordering_fields = ['id','created_date','order_at']

    filterset_fields = {
        'parent':['exact'],
    }
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
    
        parent_is_null = self.request.query_params.get('parent__isnull')
        if parent_is_null == 'true':
            queryset = queryset.filter(parent__isnull=True)
        
        return queryset

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CategoryWriteSerializers
        return super().get_serializer_class()
    
    def get_authentication_classes(self):
        return [JWTAuthentication()]
