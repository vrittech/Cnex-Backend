from django.shortcuts import render
from rest_framework import generics, status, viewsets, response
from .serializers import EmailNumberSerializer, CustomPasswordResetSerializer, TokenValidationSerializer,ContactMeSerializer
from accounts.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .sms_sender import SendSms,ContactMe
from django.db.models import Q
from django.core.cache import cache

import random
import string

otp_time_expired = 120
site_f  = "https://lims.dftqc.gov.np" #http://localhost:4200"#"https://dev-lims.netlify.app"#"https://lims.dftqc.gov.np"

class EmailCheckView(generics.GenericAPIView):

    def generate_otp(self,user):
        # Generate a random 6-digit OTP
        user = str(user)
        return user[0]+''.join(random.choices(string.digits, k=4)) + user[-1]
    
    serializer_class = EmailNumberSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = CustomUser.objects.filter(Q(email=email) | Q(phone = email)).first()
        if user:
        
            otp = self.generate_otp(user.id)

            reset_verification = "reset_password"
            subject = 'Cnex OTP'
            if '@' in email:
                email = user.email
                sendMail(email, otp,subject,reset_verification)
            else:
                SendSms(contact=email,otp=otp,message=subject)
          
            cache_key = f"password_reset_otp_{user.id}"
            cache.set(cache_key, otp, timeout=otp_time_expired)

            return response.Response(
                {
                "message": "password reset otp has been sent to your email address"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

class CustomPasswordResetView(generics.GenericAPIView):
    serializer_class = CustomPasswordResetSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
     
        user = CustomUser.objects.get(Q(email = serializer.data.get('email')) | Q(phone = serializer.data.get('email')))
        if serializer.validated_data.get('token_validate') == True:
            user.password = serializer.data.get('password')
            user.save()
            message = "Password Reset Complete"
            stat = status.HTTP_200_OK
            print(" password save ")
        else:
            message = "Password Reset not Completed"
            stat = status.HTTP_400_BAD_REQUEST
            print("password not save")

        return response.Response(
            {"message": message},
            status=stat,
        )
    

class VerifyUserPasswordToken(generics.GenericAPIView):
    serializer_class = TokenValidationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
        
        return response.Response(
            {"message": "Your Token is Validate",
             'data' : serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SendEmailVerificationLink(APIView):
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({
                'detail': 'User with this email does not exist.',
            }, status=status.HTTP_400_BAD_REQUEST)

        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # Send the token via email
        subject = 'Email Verification Token'
        verify_url = f"{site_f}/user-verification-success?pk={encoded_pk}&token={token}"
        subject = 'Email Verification Link '
        reset_verification = "verification"
        sendMail(email,verify_url,subject,reset_verification)

        return Response({
            'detail': 'Email verificatio'})

def sendMail(email, reset_url,subject,reset_verification):
    if reset_verification == "verification":
        body = f"""<body>
            <table align="center" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; font-family: Poppins; background: whitesmoke; padding: 20px; border-radius: 6px;">
                <tr>
                    <td align="center" bgcolor="#FFFFFF" style="padding: 20px;">
                        <img src="https://cnex.com.np/assets/logo-Ds_vvW8g.png" alt="" width="132" style="display: block; margin: 0 auto;">
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Cnex</p>
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Please verify your account</p>
                        <p style="text-align: center; font-weight: 400;">Click the button below to verify your account.</p>
                        <a href="{reset_url}" style="text-decoration: none; background: #0B53A7; color: #FFFFFF; padding: 10px 20px; border-radius: 3px; display: inline-block; margin-top: 15px;">Verify Your Account</a>
                        <p style="text-align: center; margin-top: 20px;">Please visit <a href="https://cnex.com.np/" style="text-decoration: none; color: #0B53A7; font-weight: 600;">https://cnex.com.np/</a> for any enquiries.</p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Tel:</span>+977 97798000000</p>
                        <p style="margin: 0; text-align: center; text-decoration: none;"><span style="font-weight: 600;">Fax:</span>+97798000000 <span style="font-weight: 600; margin-left: 10px;">E-mail:</span> info@cnex.com</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""
    else:
        body = f"""<body>
            <table align="center" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; font-family: Poppins; background: whitesmoke; padding: 20px; border-radius: 6px;">
                <tr>
                    <td align="center" bgcolor="#FFFFFF" style="padding: 20px;">
                        <img src="https://cnex.com.np/assets/logo-Ds_vvW8g.png" alt="" width="132" style="display: block; margin: 0 auto;">
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Cnex</p>
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Please change your Password</p>
                        <p style="text-align: center; font-weight: 400;">Your OTP code to reset password is</p>
                        <span style="text-decoration: none; background: #0B53A7; color: #FFFFFF; padding: 10px 20px; border-radius: 3px; display: inline-block; margin-top: 15px;">{reset_url}</span>
                        <p style="text-align: center; margin-top: 20px;">Please visit <a href="https://cnex.com.np/" style="text-decoration: none; color: #0B53A7; font-weight: 600;">https://cnex.com.np</a> for any enquiries.</p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Tel:</span> 01-5244366</p>
                        <p style="margin: 0; text-align: center; text-decoration: none;"><span style="font-weight: 600;">Phone:</span> +977 9802348565 <span style="font-weight: 600; margin-left: 10px;">E-mail:</span> support@cnex.com</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""
    html_contents = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Template</title>
            <style>
                @import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
            </style>
        </head>""" + body
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    plain_message = ""
    send_mail(subject, plain_message, email_from, recipient_list,html_message=html_contents)


class ContactmeView(generics.GenericAPIView):    
    serializer_class = ContactMeSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]
        subject = serializer.data.get('subject')
        full_name = serializer.data["full_name"]
        message = serializer.data["message"]
        phone = serializer.data.get("phone")
        
        ContactMe(email,phone,full_name,subject,message)
           
        return response.Response(
            {
            "message": "Email has sent to Cnex Owner, please kindly wait for response"
            },
            status=status.HTTP_200_OK,
        )
     
    