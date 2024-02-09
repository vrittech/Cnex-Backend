from rest_framework import serializers
from ..models import VariationOption

class VariationOptionReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'

class VariationOptionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = VariationOption
        fields = '__all__'