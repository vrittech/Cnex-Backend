from rest_framework import serializers
from ..models import HelpAndSupport

class HelpAndSupportReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpAndSupport
        fields = '__all__'

class HelpAndSupportWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = HelpAndSupport
        fields = '__all__'