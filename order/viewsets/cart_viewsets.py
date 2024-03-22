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

class CartViewsets(viewsets.ModelViewSet):
    serializer_class = CartReadSerializers
    permission_classes = [IsAuthenticated,CartPermission]
    authentication_classes = [JWTAuthentication]
    
    # pagination_class = MyPageNumberPagination
    queryset  = Cart.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CartWriteSerializers
        return super().get_serializer_class()
    
    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)
    
    @action(detail=False, methods=['post'], name="cartBulkDelete", url_path="bulk-delete")
    def cartBulkDelete(self, request):
        product_ids = request.data.get('products')
        cart_obj = Cart.objects.filter(user=request.user,products__in = product_ids).delete()
        return Response({"message": "Cart bulk deleted successfully"}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], name="getCheckOutProducts", url_path="get-checkout-products")
    def getCheckOutProducts(self, request):
        cart_ids = request.data.get('carts')
        cart_obj = Cart.objects.filter(user=request.user,id__in = cart_ids)

        total_price = 0.00
        discount = 0.00
        shipping_price = 20

        coupon_apply = False
        coupon_discount = 0

        details = []

        products = {}
        for cart in cart_obj:
            variations  = cart.variations.all()
            if not variations:
                print("variation is empty ")
                continue
            # print(cart)
            product_detail = cart.product.getDetailWithVariationList(variations)
            # print("variations::",product_detail)
            total_price = total_price + product_detail.get('tot_price')
            discount = discount + float(cart.product.discount)
            products['products'] = product_detail
            # print(products)
            details.append(products)
            products = {}
            # print(details)

        data = {
            'total_price':total_price,
            'discount':discount,
            'quantity':cart_obj.count(),
            'checkout':details,
            'shipping_price':shipping_price,
        }
        
        return Response({"message": "Cart checkout get successfully",'data':data}, status=status.HTTP_201_CREATED)


    

    