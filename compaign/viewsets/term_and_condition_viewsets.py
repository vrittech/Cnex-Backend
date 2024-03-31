from ..models import TermAndCondition
from ..serializers.term_and_condition_serializers import TermAndConditionReadSerializers,TermAndConditionWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response

class TermAndConditionViewsets(viewsets.ModelViewSet):
    serializer_class = TermAndConditionReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = TermAndCondition.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return TermAndConditionWriteSerializers
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.first())  # Serialize the first object directly
        return Response(serializer.data)
    