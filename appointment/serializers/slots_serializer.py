from rest_framework import serializers
from ..models import Slots

class SlotsReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'

class SlotsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = '__all__'
