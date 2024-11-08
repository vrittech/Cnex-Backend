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
from rest_framework.decorators import action
from reviewrating.models import Rating
from order.models import Order,OrderItem
from ..models import Category
from django.db.models import Q

class ProductViewsets(viewsets.ModelViewSet):
    serializer_class = ProductReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Product.objects.all()
    
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['title','tags__name','name','category__name','collection__name']
    ordering_fields = ['id','created_date','discount','rating','price']

    filterset_fields = {
        # 'category':['exact'],
        'product_type':['exact'],
        'price': ['exact', 'gte', 'lte'],
        'is_manage_stock':['exact'],
        'collection':['exact'],
        'collection__is_active':['exact'],
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
        
    def get_queryset(self):
        
        queryset = super().get_queryset()

        category_id = self.request.query_params.get('category')
        if category_id:
            # Get the category object
            category = Category.objects.filter(id=category_id)
            if category.exists():
                category = category.first()
                # Query products filtering by category and its parent categories recursively
                queryset = queryset.filter(Q(category=category) | Q(category__parent=category) | Q(category__parent__parent=category) ).distinct()
            else:
                queryset = Product.objects.none()

        if self.request.user.is_authenticated and self.action in ['MyReviewProducts']:
            my_rating_products = self.request.user.rating.all().values_list('product',flat=True)
            return queryset.filter(id__in = my_rating_products).order_by('-created_date')
        
        elif self.request.user.is_authenticated and self.action in ['RemainingReviewProducts']:
            order_products = Order.objects.filter(user = self.request.user).values_list('products',flat=True)
            my_rating_products = self.request.user.rating.all().values_list('product',flat=True)
            all_products = queryset.filter(id__in = order_products).exclude(id__in = my_rating_products)
            return all_products

        elif self.request.user.is_authenticated and self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
            return queryset.order_by('-created_date')

        return queryset.filter(is_publish = True).order_by('-created_date')
            
    # @method_decorator(cache_page(cache_time,key_prefix="ProductViewsets"))
    def list(self, request, *args, **kwargs):
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

    @action(detail=False, methods=['get'], name="MyReviewProducts", url_path="my-review-products")
    def MyReviewProducts(self, request,*args,**kwargs):
        return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['get'], name="RemainingReviewProducts", url_path="my-remaining-products")
    def RemainingReviewProducts(self, request,*args,**kwargs):
        return super().list(request, *args, **kwargs)

        