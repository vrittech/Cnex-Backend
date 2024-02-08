from rest_framework import serializers
from ..models import Collection

class CollectionReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class CollectionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'