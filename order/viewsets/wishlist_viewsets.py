from ..models import Wishlist
from ..serializers.wishlist_serializer import WishlistReadSerializers,WishlistWriteSerializers,AddToWishlistWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from products.models import Product

class WishlistViewsets(viewsets.ModelViewSet):
    serializer_class = WishlistReadSerializers
    permission_classes = [IsAuthenticated,WishlistPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Wishlist.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return WishlistWriteSerializers
        elif self.action in ['add_to_wishlist']:
            return AddToWishlistWriteSerializers
        return super().get_serializer_class()
    
    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'], name="add_to_wishlist", url_path="add-to-wishlist")
    def add_to_wishlist(self, request):
        product_ids = [request.data.get('products')]
        wishlist_obj = Wishlist.objects.filter(user=request.user).first()

        if wishlist_obj:
            existing_products = wishlist_obj.products.filter(pk__in=product_ids)
            if existing_products.exists():
                wishlist_obj.products.remove(*existing_products)
                return Response({"message": "Remove from wishlist successfully"}, status=status.HTTP_201_CREATED)
            else:
                products = Product.objects.filter(pk__in=product_ids)
                wishlist_obj.products.add(*products)
                return Response({"message": "Added to wishlist successfully"}, status=status.HTTP_201_CREATED)
        else:
            wishlist_obj = Wishlist.objects.create(user=request.user)
            products = Product.objects.filter(pk__in=product_ids)
            wishlist_obj.products.add(*products)
            return Response({"message": "Added to wishlist successfully"}, status=status.HTTP_201_CREATED)
    
        
    

    
    