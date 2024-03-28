from ..models import Rating
from ..serializers.rating_serializers import RatingReadSerializers,RatingWriteSerializers
from ..utilities.importbase import *

class RatingViewsets(viewsets.ModelViewSet):
    serializer_class = RatingReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Rating.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return RatingWriteSerializers
        return super().get_serializer_class()
    