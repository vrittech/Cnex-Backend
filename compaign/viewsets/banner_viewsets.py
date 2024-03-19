from ..models import Banner
from ..serializers.banner_serializers import BannerReadSerializers,BannerWriteSerializers
from ..utilities.importbase import *

class BannerViewsets(viewsets.ModelViewSet):
    serializer_class = BannerReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Banner.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return BannerWriteSerializers
        return super().get_serializer_class()
    