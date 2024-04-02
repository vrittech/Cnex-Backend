from django.urls import path
from .views import EmailCheckView, CustomPasswordResetView , VerifyUserPasswordToken,ContactmeView



urlpatterns = [
    path('get-otp-reset-email/', EmailCheckView.as_view()),
    path('password-reset/', CustomPasswordResetView.as_view(), name="reset-password"),
    path('verify-user-password-token/', VerifyUserPasswordToken.as_view(), name="VerifyUserPasswordToken"),

    path('contact-me',ContactmeView.as_view(),name="ContactmeView"),
]
