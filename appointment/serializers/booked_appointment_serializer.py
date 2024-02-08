from rest_framework import serializers
from ..models import BookedAppointment

class BookedAppointmentReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookedAppointment
        fields = '__all__'

class BookedAppointmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookedAppointment
        fields = '__all__'