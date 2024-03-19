from rest_framework import serializers
from ..models import Faqs

class FaqsReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'

class FaqsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'