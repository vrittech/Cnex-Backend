from ..models import Collection
from ..serializers.collection_serializer import CollectionReadSerializers,CollectionWriteSerializers
from ..utilities.importbase import *

class CollectionViewsets(viewsets.ModelViewSet):
    serializer_class = CollectionReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Collection.objects.all()
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CollectionWriteSerializers
        return super().get_serializer_class()