from ..models import Rating
from ..serializers.rating_serializers import RatingReadSerializers,RatingWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from accounts.models import roles
from ..utilities.permission import RatingViewsetsSetsPermission

class RatingViewsets(viewsets.ModelViewSet):
    serializer_class = RatingReadSerializers
    permission_classes = [RatingViewsetsSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Rating.objects.all().order_by('-id')

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
        if self.action in ['allRatings']:
            return super().get_queryset()
        elif self.request.user.role in [roles.SUPER_ADMIN,roles.ADMIN]:
            return super().get_queryset()
        return super().get_queryset().filter(user = self.request.user)
    
    @action(detail=False, methods=['get'], name="allRatings", url_path="get-all-rating")
    def allRatings(self, request,*args,**kwargs):
        return super().list(request, *args, **kwargs)

        

    