from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('notification', views.NotificationViewSet, basename="apis/NotificationViewSet")


urlpatterns = [
    path('', include(router.urls)),
    path('user-birthday-anniversary/',views.birthdayAnniversaryNotification,name="Test")
    # path('websocket/',views.sendNotification,name="sendNotification")
]