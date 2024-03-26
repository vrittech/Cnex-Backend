from ..models import DeliveryCharge
from ..serializers.delivery_serializers import DeliveryChargeReadSerializers,DeliveryChargeWriteSerializers
from ..utilities.importbase import *

class DeliveryChargeViewset(viewsets.ModelViewSet):
    serializer_class = DeliveryChargeReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = DeliveryCharge.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return DeliveryChargeWriteSerializers
        return super().get_serializer_class()
    