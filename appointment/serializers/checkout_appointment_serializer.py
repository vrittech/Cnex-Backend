from rest_framework import serializers
from ..models import CheckoutAppointment,Services,ServicesItems,Slots
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from ..serializers.checkout_services_items_serializers import ServicesItemsWriteSerializers
from django.db import transaction
from accounts.models import CustomUser

def getTotalServicesPrice(data):
    services = data.get('services')
    services_ids = [service.get('service') for service in services]
    user = data.get('user') #user owner permission 
    service_objs = Services.objects.filter(id__in = services_ids)
    total_service_price = service_objs.aggregate(total_price = Sum('price')).get('total_price',0)
    return {'user':user,'total_price':total_service_price}

class CheckoutAppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = CheckoutAppointment
        fields = '__all__'

class ServicesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class SlotsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'

class services_itemsSerializers(serializers.ModelSerializer):
    service = ServicesSerializers()
    slots = SlotsSerializers()
    class Meta:
        model = ServicesItems
        fields = '__all__'

class CustomUserReadSerializers_AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = "checkout_CustomUserReadSerializers_AppointmentReadSerializers"
        model = CustomUser
        fields = ['username','email','full_name','phone']

class getFailureAppointmentSerializers(serializers.ModelSerializer):
    services_items = services_itemsSerializers(many = True)
    user = CustomUserReadSerializers_AppointmentReadSerializers()
    appointment_status = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    class Meta:
        model = CheckoutAppointment
        fields = '__all__'

    def get_appointment_status(self,obj):
        return "Fail"
    
    def get_payment_status(self,obj):
        return "unpaid"

class CheckoutAppointmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CheckoutAppointment
        fields = '__all__'

    def to_internal_value(self, data):
        data = getTotalServicesPrice(data)
        print(data)
        return super().to_internal_value(data)
    
    @transaction.atomic
    def create(self, validated_data):
        instance = super().create(validated_data)
        services = self.context['request'].data.get('services')
        services = [{**service, 'checkout_appointment':instance.id,'payment_amount':Services.objects.get(id = service.get('service')).price,} for service in services]
        services_serializer = ServicesItemsWriteSerializers(data=services,many = True)
        services_serializer.is_valid(raise_exception=True)
        services_serializer.save()
        return  instance




    