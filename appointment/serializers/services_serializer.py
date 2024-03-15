from rest_framework import serializers
from ..models import Services
from .slots_serializer import SlotsWriteSerializers
import json

class ServicesReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class ServicesWriteSerializers(serializers.ModelSerializer):
    # slots = SlotsWriteSerializers(many=True)
    class Meta:
        model = Services
        fields = '__all__'
  
    def create(self, validated_data):
        slots_data = self.context['request'].data.get('slots')#validated_data.pop('slots', None)
        print(type(slots_data)) #type string
        # Parsing slots data from string to JSON
        if slots_data is not None:
            slots_data = json.loads(slots_data)#type list
        print(type(slots_data[0])) #type dictionary
        instance = super().create(validated_data)
    
        return instance