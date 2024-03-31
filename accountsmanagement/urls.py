from django.urls import path
from .views import EmailCheckView, CustomPasswordResetView , VerifyUserPasswordToken,NumberCheckView



urlpatterns = [
    path('get-otp-reset-email/', EmailCheckView.as_view()),
    path('get-otp-reset-number/', NumberCheckView.as_view()),
    path('password-reset/', CustomPasswordResetView.as_view(), name="reset-password"),
    path('verify-user-password-token/', VerifyUserPasswordToken.as_view(), name="VerifyUserPasswordToken"),
]