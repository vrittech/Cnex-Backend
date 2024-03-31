from rest_framework import serializers
from ..models import TermAndCondition

class TermAndConditionReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermAndCondition
        fields = '__all__'

class TermAndConditionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermAndCondition
        fields = '__all__'