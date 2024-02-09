from ..models import VariationGroup
from ..serializers.variation_group_serializers import VariationGroupReadSerializers,VariationGroupWriteSerializers
from ..utilities.importbase import *

class VariationGroupViewsets(viewsets.ModelViewSet):
    serializer_class = VariationGroupReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = VariationGroup.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return VariationGroupWriteSerializers
        return super().get_serializer_class()
    