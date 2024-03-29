from rest_framework import serializers
from ..models import AppRating
from accounts.models import CustomUser


class CustomUserReadSerializers_AppRatingRatingReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','full_name']

class AppRatingRatingReadSerializers(serializers.ModelSerializer):
    user = CustomUserReadSerializers_AppRatingRatingReadSerializers()
    class Meta:
        model = AppRating
        fields = '__all__'

class AppRatingWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = AppRating
        fields = '__all__'