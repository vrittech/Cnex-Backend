from ..models import Rating
from ..serializers.rating_serializer import RatingReadSerializers,RatingWriteSerializers
from ..utilities.importbase import *

class RatingViewsets(viewsets.ModelViewSet):
    serializer_class = RatingReadSerializers
    pagination_class = MyPageNumberPagination
    queryset = Rating.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminViewSetsPermission]
    swagger_schema_title = 'RatingViewsets API'
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return RatingWriteSerializers
        return super().get_serializer_class()
    