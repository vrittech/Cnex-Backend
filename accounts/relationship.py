from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Relationship,CustomUser
from .relatationshipserializer import RelationshipViewSetSerializer,UnfollowSerializer
from rest_framework import views
from rest_framework.decorators import api_view, permission_classes
# from .serializers import UnfollowSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .custompermission import RelationshipPermission
from rest_framework.response import Response


class RelationshipViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,RelationshipPermission]
    serializer_class = RelationshipViewSetSerializer
    queryset = Relationship.objects.all()

class UnfollowRelationship(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    def post(self,request):
        data = Relationship.objects.filter(followed_by_user_id=request.user, followed_to_id=request.data.get('followed_to'))
        if data.exists():
            data.delete()
            return Response({'status': 'success', 'message': 'Unfollowed successfully'})
        return Response({'status': 'error', 'message': 'Invalid data'})
        