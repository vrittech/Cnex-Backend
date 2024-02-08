from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.appointment_viewsets import AppointmentViewsets
from .viewsets.booked_appointment_viewsets import BookedAppointmentViewSets
from .viewsets.services_viewsets import ServicesViewsets
from .viewsets.slots_viewsets import SlotsViewsets

router.register('appointment',AppointmentViewsets,basename='AppointmentViewsets')
router.register('booked-appointment',BookedAppointmentViewSets,basename='BookedAppointmentViewSets')
router.register('slots-services',ServicesViewsets,basename='ServicesViewsets')
router.register('slots',SlotsViewsets,basename='slots')

urlpatterns = [
    path('',include(router.urls)),
]


