from ..models import Coupon
from ..serializers.coupon_serializers import CouponReadSerializers,CouponWriteSerializers
from ..utilities.importbase import *
from accounts import roles

class CouponViewsets(viewsets.ModelViewSet):
    serializer_class = CouponReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Coupon.objects.all().order_by('-created_date')

    def get_queryset(self):
        return super().get_queryset().filter(is_coupon_ok = True)
        if self.request.user.is_authenticated and self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(is_coupon_ok = True)

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CouponWriteSerializers
        return super().get_serializer_class()
    