from rest_framework import serializers
from ..models import ServicesItems

class ServicesItemsReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicesItems
        fields = '__all__'

class ServicesItemsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicesItems
        fields = '__all__'
