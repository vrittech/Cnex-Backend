from rest_framework import serializers
from ..models import Rating
from accounts.models import CustomUser


class CustomUserReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','full_name']

class RatingReadSerializers(serializers.ModelSerializer):
    user = CustomUserReadSerializers()
    class Meta:
        model = Rating
        fields = '__all__'

class RatingWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'