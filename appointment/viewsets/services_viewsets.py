from ..models import Services
from ..serializers.services_serializer import ServicesReadSerializers,ServicesWriteSerializers,ServicesRetrieveSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from accounts import roles

class ServicesViewsets(viewsets.ModelViewSet):
    serializer_class = ServicesReadSerializers
    # permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Services.objects.all().order_by('-id')

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(is_active = True)

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ServicesWriteSerializers
        elif self.action in ['retrieve']:
            return ServicesRetrieveSerializers
        elif self.action in ['list']:
            return super().get_serializer_class()
    
    @action(detail=False, methods=['post'], name="ServicesAvailable", url_path="get-services-available")
    def ServicesAvailable(self, request):
        date = request.data.get('date')
        service_id = request.data.get('servcie_id')
        print(date,service_id," required date.")
        services_obj = Services.objects.get(id = service_id)
        slots_available = services_obj.getServicesSlotsAvailable(date)
        return Response({'services':slots_available}, status=status.HTTP_201_CREATED)

    