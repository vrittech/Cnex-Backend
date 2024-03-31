from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth.hashers import make_password

from django.core.cache import cache

def TokenValidate(token,email):
    user = CustomUser.objects.filter(email = email)
    if user.exists():
        user = user.first()
        user_check_key = f"password_reset_otp_{user.id}"
        token_access = cache.get(user_check_key)
        if token_access == token:
            return True
    return False
    

class TokenValidationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()
    
    def validate_otp(self, value):
        # Perform your token validation logic here
        email = self.initial_data.get('email')  # Access email from initial data
        if not TokenValidate(value,email):
            raise serializers.ValidationError("Invalid token")
        return value

        
class CustomPasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=4)
    email = serializers.EmailField()

    class Meta:
        fields = '__all__'

    def validate_password(self, value):
        # Hash the password using Django's make_password function
        return make_password(value)
    
    def validate_token(self, value):
        # Perform your token validation logic here
        email = self.initial_data.get('email')  # Access email from initial data
        if not TokenValidate(value,email):
            raise serializers.ValidationError("Invalid token")
        return value
    
    def validate(self, attrs):
        attrs  =  super().validate(attrs)
 
        if TokenValidate(self.initial_data.get('token') ,self.initial_data.get('email')):
            attrs['token_validate'] = True
        else:
            attrs['token_validate'] = False
        return attrs

 
class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

 
class NumberSerializer(serializers.Serializer):
    number = serializers.CharField()
