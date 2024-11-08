from ..models import AppRating
from ..serializers.apprating_serializers import AppRatingWriteSerializers,AppRatingRatingReadSerializers
from ..utilities.importbase import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from accounts import roles

class AppRatingViewsets(viewsets.ModelViewSet):
    serializer_class = AppRatingRatingReadSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = AppRating.objects.all().order_by('-id')

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    # ordering_fields = ['']

    filterset_fields = {
        'user':['exact'],
        'rating':['exact'],
    }


    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return AppRatingWriteSerializers
        return super().get_serializer_class()
    
    def get_queryset(self):
        if self.request.method in ['allRatings']:
            return super().get_queryset().all()
        elif self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
             return super().get_queryset().all()
        
        return super().get_queryset().filter(user = self.request.user)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="allRatings", url_path="get-all-rating")
    def allRatings(self, request,*args,**kwargs):
        return super().list(request, *args, **kwargs)
        

    