from rest_framework import serializers
from .models import Relationship

class RelationshipViewSetSerializer(serializers.ModelSerializer):
    """
    Serializer class for NewsCategory model.
    """
    class Meta:
        model = Relationship
        fields = '__all__'

class UnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Relationship
        fields = '__all__'
