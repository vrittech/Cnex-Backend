from rest_framework import generics
from products.models import Product
from rest_framework import serializers
from ..utilities.pagination import MyPageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ProductSerializer_WishlistProductsView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','slug','featured_image','title','price','quantity','description','discount','category','brand']

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
    

