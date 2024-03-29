from rest_framework import serializers
from ..models import Variation,VariationOption
from .variation_option_serializers import VariationOptionWriteSerializers

class VariationOptionSerializers_VariationReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = ['id','value']

class VariationReadSerializers(serializers.ModelSerializer):
    options = VariationOptionSerializers_VariationReadSerializers(many = True)
    class Meta:
        model = Variation
        fields = '__all__'
    

class VariationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'

    def create(self, validated_data):
        variation = super().create(validated_data)
        options = self.initial_data.get('option')

        options = [{**option , 'variation':variation.id} for option in options ]
        serializers = VariationOptionWriteSerializers(data = options,many = True)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        return variation
    
    def update(self, instance, validated_data):
        created_instance = super().update(instance, validated_data)
        options = self.initial_data.get('option')
      
        for option in options:
            is_id = option.get('id')
            option['variation'] = created_instance.id

            if is_id:
                variation_option_instance = VariationOption.objects.get(id = is_id)
                serializers = VariationOptionWriteSerializers(variation_option_instance,data = option,partial=True)
                serializers.is_valid(raise_exception=True)
                serializers.save()
            else:
                serializers = VariationOptionWriteSerializers(data = option)
                serializers.is_valid(raise_exception=True)
                serializers.save()
           
        return created_instance