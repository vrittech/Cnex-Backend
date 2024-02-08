from rest_framework import serializers
from ..models import Services

class ServicesReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class ServicesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'