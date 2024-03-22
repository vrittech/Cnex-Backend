from ..models import Checkout
from ..serializers.checkout_serializer import CheckoutReadSerializers,CheckoutWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

class CheckoutViewsets(viewsets.ModelViewSet):
    serializer_class = CheckoutReadSerializers
    # permission_classes = [AdminViewSetsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Checkout.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CheckoutWriteSerializers
        return super().get_serializer_class()