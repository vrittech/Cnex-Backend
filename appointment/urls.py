from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.appointment_viewsets import AppointmentViewsets
from .viewsets.services_viewsets import ServicesViewsets
from .viewsets.slots_viewsets import SlotsViewsets

router.register('appointment',AppointmentViewsets,basename='AppointmentViewsets')
router.register('services',ServicesViewsets,basename='ServicesViewsets')

urlpatterns = [
    path('',include(router.urls)),
]


