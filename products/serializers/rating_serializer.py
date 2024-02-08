from rest_framework import serializers
from ..models import Rating

class RatingReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class RatingWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'