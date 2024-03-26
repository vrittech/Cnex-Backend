from rest_framework import serializers
from ..models import Appointment,Services,Slots
from accounts.models import CustomUser

class CustomUserReadSerializers_AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ServicesReadSerializers_AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class SlotReadSerializers_AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'

class AppointmentReadSerializers(serializers.ModelSerializer):
    user = CustomUserReadSerializers_AppointmentReadSerializers()
    service = ServicesReadSerializers_AppointmentReadSerializers()
    slots = SlotReadSerializers_AppointmentReadSerializers()
    class Meta:
        model = Appointment
        fields = '__all__'
        

class AppointmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'