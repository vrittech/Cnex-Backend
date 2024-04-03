from ..models import Cart
from ..serializers.cart_serializer import CartReadSerializers,CartWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from products.models import Product
from rest_framework import status
from ..utilities.permission  import  CartPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..viewsets.cart_to_order import CartToOrder
from coupon.models import Coupon
from ..utilities.hisab_kitab_from_karts import CartsHisabKitab


class CartViewsets(viewsets.ModelViewSet):
    serializer_class = CartReadSerializers
    permission_classes = [IsAuthenticated,CartPermission]
    authentication_classes = [JWTAuthentication]
    
    # pagination_class = MyPageNumberPagination
    queryset  = Cart.objects.all().filter(product__product_type = "product_type")

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CartWriteSerializers
        return super().get_serializer_class()
    
    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)
    
    @action(detail=False, methods=['post'], name="cartBulkDelete", url_path="bulk-delete")
    def cartBulkDelete(self, request):
        product_ids = request.data.get('products')
        cart_obj = Cart.objects.filter(user=request.user,product__in = product_ids).delete()
        return Response({"message": "Cart bulk deleted successfully"}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], name="CartToOrder", url_path="cart-checkout")
    def CartToOrder(self, request):
        coupon_code = request.data.get('coupon_code')
        coupon_obj = None
        if coupon_code:
            coupon_obj = Coupon.objects.filter(code = coupon_code)
            if coupon_obj.exists() and coupon_obj.first().is_verify == True:
                pass
            else:
                return Response({"message": "Either coupon not exists or it is expired"}, status=status.HTTP_400_BAD_REQUEST)
            
        cart_ids = request.data.get('carts')
        order_ids = CartToOrder(request,cart_ids,coupon_obj)
        return Response({"message": "checkout successfully",'order_id':order_ids}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], name="getCheckOutProducts", url_path="get-checkout-products")
    def getCheckOutProducts(self, request):
        data = CartsHisabKitab(request)
        return Response({"message": data.get('message'),'data':data}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], name="cartCount", url_path="my-total-cart")
    def cartCount(self, request):
        my_cart = self.get_queryset().count()
        return Response({"my_cart_quantity":my_cart}, status=status.HTTP_201_CREATED)
    

    
    

    