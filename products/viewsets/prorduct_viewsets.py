from ..models import Product
from ..serializers.product_serializer import ( ProductReadSerializers,
                                              ProductWriteSerializers,
                                              ProductRetrieveAdminSerializers,
                                              ProductRetrieveSerializers,
                                              ProductReadAdminSerializers
                                        )
from ..utilities.importbase import *
from accounts import roles

class ProductViewsets(viewsets.ModelViewSet):
    serializer_class = ProductReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Product.objects.all()
    swagger_schema_title = 'ProductViewsets API'
    lookup_field = 'slug'
    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return ProductWriteSerializers
        elif self.action in ['retrieve']:
            if self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
                return ProductRetrieveAdminSerializers
            else:
                return ProductRetrieveSerializers
            
        elif self.action in ['list']:
            if self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
                return ProductReadAdminSerializers
            else:
                return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        file_uploaded = request.FILES  # Access the uploaded file   
        print(file_uploaded)
        
        return super().create(request, *args, **kwargs)
    