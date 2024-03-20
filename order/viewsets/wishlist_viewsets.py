from ..models import Wishlist
from ..serializers.wishlist_serializer import WishlistReadSerializers,WishlistWriteSerializers
from ..utilities.importbase import *
from rest_framework.permissions import IsAuthenticated

class WishlistViewsets(viewsets.ModelViewSet):
    serializer_class = WishlistReadSerializers
    permission_classes = [IsAuthenticated,WishlistPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Wishlist.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return WishlistWriteSerializers
        return super().get_serializer_class()
    