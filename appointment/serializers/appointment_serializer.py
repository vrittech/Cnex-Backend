from rest_framework import serializers
from ..models import Appointment,Services,Slots,CheckoutAppointment,ServicesItems
from accounts.models import CustomUser
from django.core.exceptions import ValidationError

class CustomUserReadSerializers_AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUserReadSerializers_AppointmentReadSerializers"
        model = CustomUser
        fields = ['username','email','full_name','phone']

class ServicesReadSerializers_AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class SlotReadSerializers_AppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'

class ServicesItems_AppointmentReadSerializers(serializers.ModelSerializer):
    service = ServicesReadSerializers_AppointmentReadSerializers()
    slots = SlotReadSerializers_AppointmentReadSerializers()
    class Meta:
        model = ServicesItems
        fields = '__all__'

class CheckoutAppointment_AppointmentReadSerializers(serializers.ModelSerializer):
    services_items = ServicesItems_AppointmentReadSerializers(many = True)
    class Meta:
        model = CheckoutAppointment
        fields = '__all__'

class AppointmentReadSerializers(serializers.ModelSerializer):
    user = CustomUserReadSerializers_AppointmentReadSerializers()
    checkout_appointment = CheckoutAppointment_AppointmentReadSerializers()
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate_slots(self,value):
        if value.is_slots_available(self.instance.appointment_date):
            return value
        else:
            raise ValidationError("One or more selected slots are not available for the appointment date.")