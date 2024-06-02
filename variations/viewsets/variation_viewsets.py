from ..models import Variation
from ..serializers.variation_serializers import VariationReadSerializers,VariationWriteSerializers
from ..utilities.importbase import *

class VariationViewsets(viewsets.ModelViewSet):
    serializer_class = VariationReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Variation.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return VariationWriteSerializers
        return super().get_serializer_class()
    