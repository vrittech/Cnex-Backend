from rest_framework import serializers
from ..models import Appointment

class AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'