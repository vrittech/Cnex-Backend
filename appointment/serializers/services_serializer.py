from rest_framework import serializers
from ..models import Services,Slots
from .slots_serializer import SlotsWriteSerializers
import json

class SlotsReadSerializers_ServicesReadSerializers(serializers.ModelSerializer):
    remaining_slots = serializers.SerializerMethodField()
    class Meta:
        model = Slots
        fields = '__all__'
    def get_remaining_slots(self,obj):
        return int(obj.number_of_staffs)-int(obj.appointment.all().count())

class ServicesReadSerializers(serializers.ModelSerializer):
    slots = SlotsReadSerializers_ServicesReadSerializers(many = True)
    class Meta:
        model = Services
        fields = '__all__'

class ServicesRetrieveSerializers(serializers.ModelSerializer):
    slots = SlotsReadSerializers_ServicesReadSerializers(many = True)
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
    
    def update(self, instance, validated_data):
        slots_data = self.context['request'].data.get('slots')
        service_instance = super().update(instance, validated_data)

        if slots_data is not None:
            slots_data = json.loads(slots_data)
            for slot_data in slots_data:
                slot_id = slot_data.get('id')  # Check if ID is provided
                print(slot_id," slot id")
                if slot_id:
                    slot_instance = Slots.objects.get(id=slot_id, services=service_instance.id)  # Retrieve the object to update
                    print(slot_instance," slot instance")
                else:
                    slot_data['services'] = service_instance.id  # Set the service for new slot
                    slot_instance = None  # Set slot_instance to None for new slot creation
                
                serializer = SlotsWriteSerializers(slot_instance, data=slot_data, partial=True)  # Initialize

                # Validate and update/create the serializer
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return service_instance

