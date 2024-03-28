from ..models import Rating
from ..serializers.rating_serializers import RatingReadSerializers,RatingWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class RatingViewsets(viewsets.ModelViewSet):
    serializer_class = RatingReadSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Rating.objects.all()

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['rating']

    filterset_fields = {
        'user':['exact'],
        'product':['exact'],
        'rating':['exact'],
    }


    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return RatingWriteSerializers
        return super().get_serializer_class()
    
    def get_queryset(self):
        if self.request.method in ['allRatings']:
            return super().get_queryset().all()
        return super().get_queryset().filter(user = self.request.user)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="allRatings", url_path="get-all-rating")
    def allRatings(self, request,*args,**kwargs):
        return super().list(request, *args, **kwargs)
        

    