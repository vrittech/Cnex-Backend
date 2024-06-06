from ..models import CheckoutAppointment
from ..serializers.checkout_appointment_serializer import CheckoutAppointmentReadSerializers,CheckoutAppointmentWriteSerializers,getFailureAppointmentSerializers
from ..utilities.importbase import *
from accounts import roles
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Services
from django.db.models import Sum
from rest_framework import serializers
from ..utilities.check_services_available import checkServicesAvailable
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from ..models import Appointment

class CheckoutAppointmentViewsets(viewsets.ModelViewSet):
    serializer_class = CheckoutAppointmentReadSerializers
    permission_classes = [IsAuthenticated]    
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset  = CheckoutAppointment.objects.all()

    def get_serializer_class(self):
        if self.action in ['create','update','partial_update']:
            return CheckoutAppointmentWriteSerializers
        elif self.action in ['getFailureAppointment']:
            return getFailureAppointmentSerializers
        return super().get_serializer_class()

        
    def get_queryset(self):
        if self.request.user.role in [roles.ADMIN,roles.SUPER_ADMIN]:
            if self.action in ['getFailureAppointment']:
                order_appointments = list(Appointment.objects.all().values_list('checkout_appointment',flat = True))
                return super().get_queryset().filter(~Q(id__in = order_appointments))
            return super().get_queryset()
        else:
            return super().get_queryset().filter(user_id = self.request.user.id)
    
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

    @action(detail=False, methods=['post'], name="checkOutAppointment", url_path="services-checkout")
    def checkOutAppointment(self, request):
        services = request.data.get('services')
        if not checkServicesAvailable(services):
            return Response({'message':'some services are not available at given date'},status=status.HTTP_400_BAD_REQUEST)
        services_ids = [service.get('service') for service in services]
        user = request.data.get('user') #user owner permission 
        service_objs = Services.objects.filter(id__in = services_ids)
        total_service_price = service_objs.aggregate(total_price = Sum('price')).get('total_price',0)
        services_serializer = ServicesReadSerializers_Checkout(service_objs,many = True)
        return Response({"message": "checkout successfully",'total_price':total_service_price,'services':services_serializer.data}, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        services = request.data.get('services')
        if not checkServicesAvailable(services):
            return Response({'message':'some services are not available at given date'},status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="getFailureAppointment", url_path="cart-appointment")
    def getFailureAppointment(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ServicesReadSerializers_Checkout(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['name','id','price']