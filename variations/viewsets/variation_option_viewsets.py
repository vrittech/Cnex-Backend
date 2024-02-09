from ..models import VariationOption
from ..serializers.variation_option_serializers import VariationOptionReadSerializers,VariationOptionWriteSerializers
from ..utilities.importbase import *

class VariationOptionViewsets(viewsets.ModelViewSet):
    serializer_class = VariationOptionReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = VariationOption.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return VariationOptionWriteSerializers
        return super().get_serializer_class()
    