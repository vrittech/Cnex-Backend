from ..models import Review
from ..serializers.review_serializers import ReviewReadSerializers,ReviewWriteSerializers
from ..utilities.importbase import *

class ReviewViewsets(viewsets.ModelViewSet):
    serializer_class = ReviewReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Review.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ReviewWriteSerializers
        return super().get_serializer_class()
    