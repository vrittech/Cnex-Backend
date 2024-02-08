from ..models import Cart
from ..serializers.cart_serializer import CartReadSerializers,CartWriteSerializers
from ..utilities.importbase import *

class CartViewsets(viewsets.ModelViewSet):
    serializer_class = CartReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Cart.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CartWriteSerializers
        return super().get_serializer_class()
    