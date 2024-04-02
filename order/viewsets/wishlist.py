from rest_framework import generics
from products.models import Product
from rest_framework import serializers
from ..utilities.pagination import MyPageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from order.models import Wishlist

from products.models import Product,Category,Brand


class BrandReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = "wishlist_get"
        model = Brand
        fields = ['name']

class ParentCategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = "wishlist_get"
        model = Category
        fields = ['name','id']

class CategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    parent = ParentCategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers()
    class Meta:
        ref_name = "wishlist_get"
        model = Category
        fields = ['name','parent','id']

class ProductSerializer_WishlistProductsView(serializers.ModelSerializer):
    category = CategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers()
    brand = BrandReadSerializers_WishlistReadSerializers()
    class Meta:
        model = Product
        fields =  ['product_id','has_variations','is_stock','total_sale','name','title','slug','public_id','description','price','category','quantity','brand','discount','featured_image','product_type','average_rating','total_rating']

class WishlistProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer_WishlistProductsView
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id','created_date']

    filterset_fields = {
        'product_type':['exact'],
    }

    def get_queryset(self):
        wishlist = Wishlist.objects.filter(user = self.request.user)
        if wishlist.exists():
            return wishlist.first().products.all()
        else:
            return Product.objects.none()
        

