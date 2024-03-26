from ..models import Banner
from ..serializers.banner_serializers import BannerReadSerializers,BannerWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from rest_framework import status

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

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response({"message": "Object deleted successfully"}, status=status.HTTP_200_OK)
    
    