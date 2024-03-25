from ..models import Payment
from ..serializers.payment_serializers import PaymentReadSerializers,PaymentWriteSerializers
from ..utilities.importbase import *

class PaymentViewsets(viewsets.ModelViewSet):
    serializer_class = PaymentReadSerializers
    permission_classes = [AdminViewSetsPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = Payment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return PaymentWriteSerializers
        return super().get_serializer_class()
    