from ..models import Product
from ..serializers.product_serializer import ( ProductReadSerializers,
                                              ProductWriteSerializers,
                                              ProductRetrieveAdminSerializers,
                                              ProductRetrieveSerializers,
                                              ProductReadAdminSerializers
                                        )
from ..utilities.importbase import *
from accounts import roles

cache_time = 30 # 300 is 5 minutes
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

class ProductViewsets(viewsets.ModelViewSet):
    serializer_class = ProductReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Product.objects.all()
    
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['title','tags__name','name','category__name','collection__name']
    ordering_fields = ['id','created_date','discount','rating']

    filterset_fields = {
        'category':['exact'],
        'product_type':['exact'],
        'price': ['exact', 'gte', 'lte'],
    }

    lookup_field = 'slug'
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductWriteSerializers
        elif self.action in ['retrieve']:
            if self.request.user.is_authenticated:
                if self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
                    return ProductRetrieveAdminSerializers
                else:
                    return ProductRetrieveSerializers
            else:
                return ProductRetrieveSerializers
            
        elif self.action in ['list']:
            if self.request.user.is_authenticated and self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
                return ProductReadAdminSerializers
            else:
                return super().get_serializer_class()
        else:
            return super().get_serializer_class()
            
    # @method_decorator(cache_page(cache_time,key_prefix="ProductViewsets"))
    def list(self, request, *args, **kwargs):
        print(" with out cache")
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Perform the default object creation
        instance = serializer.save()
        tags_data = self.request.data.get('tag_manager', [])
        if len(tags_data) != 0:
            instance.save_tags(tags_data)
        else:
            print("tags error ")