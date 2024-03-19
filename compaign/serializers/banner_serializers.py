from rest_framework import serializers
from ..models import Banner

class BannerReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BannerWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'