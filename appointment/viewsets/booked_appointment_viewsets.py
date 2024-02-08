from ..models import BookedAppointment
from ..serializers.booked_appointment_serializer import BookedAppointmentReadSerializers,BookedAppointmentWriteSerializers
from ..utilities.importbase import *

class BookedAppointmentViewSets(viewsets.ModelViewSet):
    serializer_class = BookedAppointmentReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = BookedAppointment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return BookedAppointmentWriteSerializers
        return super().get_serializer_class()
    