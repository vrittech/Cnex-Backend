from ..models import ShippingAddress
from accounts.serializers.shipping_address_serializers import ShippingAddressReadSerializers,ShippingAddressWriteSerializers
from ..utilities.importbase import *

class ShippingAddressViewsets(viewsets.ModelViewSet):
    serializer_class = ShippingAddressReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = ShippingAddress.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ShippingAddressWriteSerializers
        return super().get_serializer_class()
    