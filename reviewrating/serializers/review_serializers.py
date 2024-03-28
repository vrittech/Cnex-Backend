from rest_framework import serializers
from ..models import Review

class ReviewReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'