from ..models import Faqs
from ..serializers.faqs_serializers import FaqsReadSerializers,FaqsWriteSerializers
from ..utilities.importbase import *

class FaqsViewsets(viewsets.ModelViewSet):
    serializer_class = FaqsReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Faqs.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return FaqsWriteSerializers
        return super().get_serializer_class()
    