from ..models import Services
from ..serializers.services_serializer import ServicesReadSerializers,ServicesWriteSerializers,ServicesRetrieveSerializers
from ..utilities.importbase import *

class ServicesViewsets(viewsets.ModelViewSet):
    serializer_class = ServicesReadSerializers
    # permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Services.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ServicesWriteSerializers
        elif self.action in ['retrieve']:
            return ServicesRetrieveSerializers
        elif self.action in ['list']:
            return super().get_serializer_class()
    