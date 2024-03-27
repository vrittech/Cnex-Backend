from ..models import Slots
from ..serializers.slots_serializer import SlotsReadSerializers,SlotsWriteSerializers
from ..utilities.importbase import *

class SlotsViewsets(viewsets.ModelViewSet):
    serializer_class = SlotsReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Slots.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return SlotsWriteSerializers
        return super().get_serializer_class()
    