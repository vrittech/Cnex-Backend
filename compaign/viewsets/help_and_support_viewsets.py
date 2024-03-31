from ..models import HelpAndSupport
from ..serializers.help_and_support_serializers import HelpAndSupportReadSerializers,HelpAndSupportWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response

class HelpAndSupportViewsets(viewsets.ModelViewSet):
    serializer_class = HelpAndSupportReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    # pagination_class = MyPageNumberPagination
    queryset  = HelpAndSupport.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return HelpAndSupportWriteSerializers
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.first())  # Serialize the first object directly
        return Response(serializer.data)
    