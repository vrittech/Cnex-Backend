from rest_framework import serializers
from ..models import Services,Slots
from .slots_serializer import SlotsWriteSerializers
import json

class ServicesReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class ServicesWriteSerializers(serializers.ModelSerializer):
    slots = SlotsWriteSerializers(many=True,read_only = True)
    class Meta:
        model = Services
        fields = '__all__'

    def create(self, validated_data):
        slots_data = self.context['request'].data.get('slots')
        # Create the Services instance
        service_instance = Services.objects.create(**validated_data)

        if slots_data is not None:
            # Parse slots data from string to JSON
            slots_data = json.loads(slots_data)
            # Add the service_instance to each slot_data dictionary
            for slot_data in slots_data:
                slot_data['services'] = service_instance.id

            # Initialize SlotsWriteSerializers with the modified slots_data
            slots_serializer = SlotsWriteSerializers(data=slots_data, many=True)
            
            # Validate the serializer
            slots_serializer.is_valid(raise_exception=True)
            
            # Save the validated data (creating Slots instances)
            slots_serializer.save()

        return service_instance