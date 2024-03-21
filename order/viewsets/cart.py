from rest_framework import generics
from products.models import Product
from rest_framework import serializers
from ..utilities.pagination import MyPageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from order.models import Cart

from products.models import Product,Category,Brand


class BrandReadSerializers_CartReadSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = "Cart_get"
        model = Brand
        fields = ['name']

class ParentCategoryReadSerializers_ProductReadSerializers_CartReadSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = "Cart_get"
        model = Category
        fields = ['name','id']

class CategoryReadSerializers_ProductReadSerializers_CartReadSerializers(serializers.ModelSerializer):
    parent = ParentCategoryReadSerializers_ProductReadSerializers_CartReadSerializers()
    class Meta:
        ref_name = "Cart_get"
        model = Category
        fields = ['name','parent','id']

class ProductSerializer_CartProductsView(serializers.ModelSerializer):
    category = CategoryReadSerializers_ProductReadSerializers_CartReadSerializers()
    brand = BrandReadSerializers_CartReadSerializers()
    class Meta:
        model = Product
        fields =  ['name','title','slug','public_id','description','price','category','quantity','brand','discount','featured_image','product_type','average_rating','total_rating']

class CartProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer_CartProductsView
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        carts = Cart.objects.filter(user = self.request.user)
        if carts.exists():
            return carts.first().products.all()
        else:
            return Product.objects.none()
        