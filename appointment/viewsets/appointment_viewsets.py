from ..models import Appointment
from ..serializers.appointment_serializer import AppointmentReadSerializers,AppointmentWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import  IsAuthenticated
from accounts import roles
from rest_framework.decorators import action
from rest_framework.response import Response

class AppointmentViewsets(viewsets.ModelViewSet):
    serializer_class = AppointmentReadSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Appointment.objects.all().order_by('-id')

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    filterset_fields = {
        'payment_status':['exact'],
        'appointment_status':['exact'],
    }

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return AppointmentWriteSerializers
        return super().get_serializer_class()
    
    def get_queryset(self):
        if self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(user = self.request.user.id)
        
    
    