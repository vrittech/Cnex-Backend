from rest_framework import serializers
from ..models import PrivacyPolicy

class PrivacyPolicyReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class PrivacyPolicyWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'