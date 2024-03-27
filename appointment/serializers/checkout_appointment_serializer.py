from rest_framework import serializers
from ..models import CheckoutAppointment

class CheckoutAppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = CheckoutAppointment
        fields = '__all__'

class CheckoutAppointmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CheckoutAppointment
        fields = '__all__'
