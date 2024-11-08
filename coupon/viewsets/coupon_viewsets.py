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

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['code','discount_type']
    ordering_fields = ['id']

    filterset_fields = {
        'discount':['gte','lte'],
        'is_active':['exact'],
        'is_expired':['exact'],
    }


    def get_queryset(self):
        # return super().get_queryset().filter(is_coupon_ok = True)
       
        if self.request.user.is_authenticated and self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
            return super().get_queryset()
        else:
            coupons = super().get_queryset().filter(is_active = True)
            valid_coupons = [coupon.id for coupon in coupons if coupon.is_coupon_ok]
            return coupons.filter(id__in = valid_coupons)

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CouponWriteSerializers
        return super().get_serializer_class()
    