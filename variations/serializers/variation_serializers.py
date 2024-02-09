from rest_framework import serializers
from ..models import Variation

class VariationReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'

class VariationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'