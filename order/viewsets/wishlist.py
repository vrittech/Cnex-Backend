from rest_framework import generics
from products.models import Product
from rest_framework import serializers
from ..utilities.pagination import MyPageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated



from products.models import Product,Category,Brand


class BrandReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

class ParentCategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','id']

class CategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers(serializers.ModelSerializer):
    parent = ParentCategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers()
    class Meta:
        model = Category
        fields = ['name','parent','id']

class ProductSerializer_WishlistProductsView(serializers.ModelSerializer):
    category = CategoryReadSerializers_ProductReadSerializers_WishlistReadSerializers()
    brand = BrandReadSerializers_WishlistReadSerializers()
    class Meta:
        model = Product
        fields =  ['name','title','slug','public_id','description','price','category','quantity','brand','discount','featured_image','product_type','average_rating','total_rating']

class WishlistProductsList(generics.ListAPIView):
    serializer_class = ProductSerializer_WishlistProductsView
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination

    def get_queryset(self):
        print("getting whshslist")
        # Retrieve the wishlist belonging to the current user
        wishlist = self.request.user.wishlists
        # Return the products associated with the wishlist
        return wishlist.products.all()
    

