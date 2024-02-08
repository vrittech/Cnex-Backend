from rest_framework import serializers
from ..models import Collection

class CollectionReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fiels = '__all__'

class CollectionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fiels = '__all__'