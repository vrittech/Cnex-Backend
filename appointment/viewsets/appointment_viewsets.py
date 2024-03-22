from ..models import Appointment
from ..serializers.appointment_serializer import AppointmentReadSerializers,AppointmentWriteSerializers
from ..utilities.importbase import *

class AppointmentViewsets(viewsets.ModelViewSet):
    serializer_class = AppointmentReadSerializers
    # permission_classes = [AdminViewSetsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Appointment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return AppointmentWriteSerializers
        return super().get_serializer_class()
    