from ..models import PrivacyPolicy
from ..serializers.privacy_policy_serializers import PrivacyPolicyReadSerializers,PrivacyPolicyWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response

class PrivacyPolicyViewsets(viewsets.ModelViewSet):
    serializer_class = PrivacyPolicyReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    # pagination_class = MyPageNumberPagination
    queryset  = PrivacyPolicy.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return PrivacyPolicyWriteSerializers
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset.first())  # Serialize the first object directly
        return Response(serializer.data)
    