from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.dilevery_viewsets import DeliveryChargeViewset

router.register('delivery-charge',DeliveryChargeViewset,basename='DeliveryChargeViewset')

urlpatterns = [
    path('',include(router.urls)),
]


