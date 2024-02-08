from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics

from .models import CustomUser

from . import roles
from .roles import roles_data

from accounts.serializers.custom_user_serializers import LoginSerializer
from accounts.serializers.custom_user_serializers import (
    CustomUserReadSerializer,CustomUserSerializer, GroupSerializer, 
    PermissionSerializer,RoleSerializer,CustomUserReadLimitedSerializer,
    UserDetailsSerializer,CustomUserReadLimitedSerializer_1
    )

from .custompermission import AccountPermission,AllUserDataPermission
from .pagination import PageNumberPagination

from .google_virify import VerifyGoogleToken

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
cache_time = 300 # 300 is 5 minute


class CustomUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # permission_classes = [Account]
    serializer_class = CustomUserReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','phone','department_name']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'role': ['exact'],

        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }

    authentication_classes = [JWTAuthentication]
    permission_classes = [AccountPermission]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CustomUserSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        user = self.request.user
        queryset =  CustomUser.objects.all()
        
        if not user.is_authenticated:
            query = CustomUser.objects.none()
        elif user.role == roles.SUPER_ADMIN: 
            query = queryset       
        elif user.role == roles.ADMIN: 
            query = queryset.filter(is_active = True)
        else:
            query = queryset.filter(id=user.id,is_active = True)
        return query.order_by("-created_date")
    
    # @method_decorator(cache_page(cache_time,key_prefix="CustomUser"))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    # @method_decorator(cache_page(cache_time,key_prefix="CustomUser"))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_active:
            # If the user is active, mark them as inactive
        
            instance.is_active = False
            instance.delete= "delete"
            instance.save()
            # Create a custom response
            response_data = {
                "message": "User Account marked as inactive"
            }
        else:
            # If the user is already inactive, return a custom error response
            response_data = {
                "message": "User Account is already inactive"
            }

        # Return the custom response
        return Response(response_data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

    
        response_data = {
            "message": "Account created successfully",
            "data": serializer.data
        }

            # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)


class RoleViewSet(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]  
    
    def get(self,request,format=None):
        serializer = RoleSerializer(data=roles_data,many=True)
        serializer.is_valid()
        serialized_data = serializer.data
    
        return Response({"roles": serialized_data},status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "Group created successfully",
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
            "message": "Group updated successfully",
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
            "message": "Group deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

    
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name','code_name','is_verified']
    ordering_fields = ['id','name']

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    

class PermissionAllDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self, request, format=None):
        object = Permission.objects.all().delete()
        return Response({'message': 'All permission delete successful'}, status=status.HTTP_200_OK)

class CheckTokenExpireView(APIView): 
    def get(self, request, format=None):
        # Get the token from the request headers or query parameters
        try:
            raw_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        except:
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Verify the access token
            access_token = AccessToken(raw_token)
            access_token.verify()

            # If the token is valid and not expired
            return Response({'valid': True}, status=status.HTTP_200_OK)

        except TokenError:
            # If the token is expired or invalid
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

    
# Create your views here.
class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        username_or_email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user using either username or email
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            user = authenticate(request, email=username_or_email, password=password)

        # If the user is authenticated, log them in and generate tokens
        if user is not None:
            if user.is_active == False:
                return Response({'error': 'Your Account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            user_obj = CustomUserSerializer(request.user,context={'request': request}) 
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_obj.data,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)

        # If the user is not authenticated, return an error message
        else:
            from django.db.models import Q
            user_obj = CustomUser.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
            if user_obj.exists():
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid username/email'}, status=status.HTTP_401_UNAUTHORIZED)


class userLimitedData(generics.ListAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]


    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','phone']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'role': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }
    
    def get_queryset(self):
        users = CustomUser.objects.filter(role = roles.USER,is_active = True)
        return users

    def get_serializer_class(self):
        return CustomUserReadLimitedSerializer
    
    #m@method_decorator(cache_page(cache_time,key_prefix="CustomUser"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AllUserData(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,] #AllUserDataPermission
    pagination_class =  PageNumberPagination

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','phone']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'role': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }
    
    def get_queryset(self):
        users = CustomUser.objects.all().order_by('id')
        return users

    def get_serializer_class(self):
        return CustomUserReadLimitedSerializer_1
    
    #m@method_decorator(cache_page(cache_time,key_prefix="CustomUser"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserDetailsView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailsSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = "username"
    # permission_classes = [IsAuthenticated]


class GoogleLogin(APIView):
    @csrf_exempt
    def post(self, request):
    
        google_id_token = request.data.get('idToken',False)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name','')
        print(first_name,last_name)
        if google_id_token == False:
            return Response({'error': 'No ID token provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        idinfo,is_verify = VerifyGoogleToken(google_id_token)
        if idinfo:
            user,success_user = createGoogleAccount(idinfo,first_name,last_name)
        else:
            return Response({'error': 'Invalid ID token.'}, status=status.HTTP_401_UNAUTHORIZED)
   
        # If the user is authenticated, log them in and generate tokens
        if success_user == True:
            if user.is_active == False:
                return Response({'error': 'Your Account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            # login(request, user)
            refresh = RefreshToken.for_user(user)
            user_obj = CustomUserSerializer(user,context={'request': request}) 
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_obj.data,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)

        # If the user is not authenticated, return an error message
        else:
            return Response({'error': 'Google Token Failed to verify'}, status=status.HTTP_401_UNAUTHORIZED)

def createGoogleAccount(idinfo,first_name,last_name):
    email = idinfo.get('email')
    first_name = first_name
    last_name = last_name
    username = email.split('@')[0]
    image = idinfo.get('picture')
    print(" creating user ")
    user = CustomUser.objects.filter(email = email)
    if user.exists():
        user = CustomUser.objects.get(email = email)
        print(user  , " user already exists")
    else:    
        user = CustomUser.objects.create(email = email , first_name = first_name , last_name = last_name, username=username,role = 5,old_password_change_case = False,provider = 2)
        print(user, " creating user")
    return user , True

   


