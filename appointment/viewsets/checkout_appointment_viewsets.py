from ..models import CheckoutAppointment
from ..serializers.checkout_appointment_serializer import CheckoutAppointmentReadSerializers,CheckoutAppointmentWriteSerializers
from ..utilities.importbase import *

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class CheckoutAppointmentViewsets(viewsets.ModelViewSet):
    serializer_class = CheckoutAppointmentReadSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = CheckoutAppointment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CheckoutAppointmentWriteSerializers
        return super().get_serializer_class()
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'service': openapi.Schema(type=openapi.TYPE_INTEGER),
                'slots': openapi.Schema(type=openapi.TYPE_INTEGER),
                'appointment_date':openapi.Schema(type=openapi.TYPE_STRING),
                'user':openapi.Schema(type=openapi.TYPE_INTEGER)
            },
            required=['service', 'slots','appointment_date','user']
        ),
        operation_summary="",
        operation_description="",
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)