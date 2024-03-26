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
        cart_ids = request.data.get('carts')
        coupon_code = request.data.get('coupon_code')

        coupon_discount = 0
        coupon_apply = False

        message = "Cart checkout get successfully"
        coupon_status = status.HTTP_201_CREATED
    
        if coupon_code:
            coupon_obj = Coupon.objects.filter(code = coupon_code)
            if coupon_obj.exists() and coupon_obj.first().is_verify == True:
                coupon_apply = True
                coupon_discount = coupon_obj.first().discount
            else:
                message = "Either coupon not exists or it is expired"
                
            
        cart_obj = Cart.objects.filter(user=request.user,id__in = cart_ids)

        total_price = 0.00
        discount = 0.00
        shipping_price = 20

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
            'coupon_apply':coupon_apply,
            'coupon_discount':coupon_discount,
        }
        
        return Response({"message": message,'data':data}, status=coupon_status)

    
    @action(detail=False, methods=['post'], name="getCheckOutProductsBuyNow", url_path="get-checkout-products-buy-now")
    def getCheckOutProductsBuyNow(self, request):
        product_id = request.data.get('products')
        coupon_code = request.data.get('coupon_code')
        prod_quantity = request.data.get('quantity')
        prod_variations = request.data.get('variations')

        print("buy now request data ::",request.data)

        coupon_discount = 0
        coupon_apply = False

        message = "Cart checkout get successfully"
        coupon_status = status.HTTP_201_CREATED
    
        if coupon_code:
            coupon_obj = Coupon.objects.filter(code = coupon_code)
            if coupon_obj.exists() and coupon_obj.first().is_verify == True:
                coupon_apply = True
                coupon_discount = coupon_obj.first().discount
            else:
                message = "Either coupon not exists or it is expired"
                
            
        product_objs = Product.objects.filter(id = product_id)

        total_price = 0.00
        discount = 0.00
        shipping_price = 20

        details = []

        products = {}
        for prod in product_objs:
            variations  = prod_variations
            if not variations:
                print("variation is empty ")
                continue
            # print(cart)
            product_detail = prod.getDetailWithVariationList(variations)
            # print("variations::",product_detail)
            total_price = total_price + product_detail.get('tot_price')
            discount = discount + float(prod.discount)
            products['products'] = product_detail
            # print(products)
            details.append(products)
            products = {}
            # print(details)

        data = {
            'total_price':total_price,
            'discount':discount,
            'quantity':prod_quantity,
            'checkout':details,
            'shipping_price':shipping_price,
            'coupon_apply':coupon_apply,
            'coupon_discount':coupon_discount,
        }
        
        return Response({"message": message,'data':data}, status=coupon_status)


    

    
    

    