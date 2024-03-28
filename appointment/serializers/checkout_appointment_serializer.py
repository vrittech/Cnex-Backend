from rest_framework import serializers
from ..models import CheckoutAppointment,Services
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from ..serializers.checkout_services_items_serializers import ServicesItemsWriteSerializers
from django.db import transaction

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




    