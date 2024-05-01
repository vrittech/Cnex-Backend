from ..models import Coupon
from ..serializers.coupon_serializers import CouponReadSerializers,CouponWriteSerializers
from ..utilities.importbase import *

class CouponViewsets(viewsets.ModelViewSet):
    serializer_class = CouponReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Coupon.objects.all().order_by('-created_date')

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CouponWriteSerializers
        return super().get_serializer_class()
    