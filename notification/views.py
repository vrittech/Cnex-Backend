from django.shortcuts import render
from rest_framework import viewsets
from . models import Notification
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination,PageNumberPagination
from rest_framework.response import Response
from .serializer import NotificationWriteSerializer,NotificationReadSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .custom_filters import CustomFilter
from account import roles
from django.db.models import Q
from .custompermission import NotificationPermission
from django.http import  HttpResponse
from datetime import date

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
cache_time = 300 # 300 is 5 minutes
from account.models import CustomUser
from .handle_notification import NotificationHandler

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):

    queryset = Notification.objects.all().order_by("-created_date")
    serializer_class = NotificationReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['notification_type','is_read']
    filterset_class = CustomFilter
    search_fields = ['notification_type']

    authentication_classes = [JWTAuthentication]
    permission_classes = [NotificationPermission]
    
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            query = Notification.objects.filter(to_notification__id = user.id)  
        else:
            query = Notification.objects.none()    
        return query.order_by("-created_date")
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NotificationWriteSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "Notification created successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "Notification updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "Notification category deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

def birthdayAnniversaryNotification(request):
    today_date = date.today()
    users_with_birthday = CustomUser.objects.filter(dob__month=today_date.month, dob__day=today_date.day)
    users_with_anniversary = CustomUser.objects.filter(created_date__month=today_date.month, created_date__day=today_date.day)
    
    for user in users_with_birthday:
        print(f"Today is the birthday of {user.username}")
        NotificationHandler(user,request,"BirthDay",'CustomUser')
    
    for user in users_with_anniversary:
        print(f"Today is the anneversary of {user.created_date}")
        NotificationHandler(user,request,"Anniversary",'CustomUser')

    return HttpResponse("sent notification completed")

