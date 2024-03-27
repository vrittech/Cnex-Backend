from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.appointment_viewsets import AppointmentViewsets
from .viewsets.services_viewsets import ServicesViewsets
from .viewsets.slots_viewsets import SlotsViewsets
from .viewsets.checkout_appointment_viewsets import CheckoutAppointmentViewsets

router.register('appointment',AppointmentViewsets,basename='AppointmentViewsets')
router.register('services',ServicesViewsets,basename='ServicesViewsets')
router.register('checkout-appointment',CheckoutAppointmentViewsets,basename='CheckoutAppointmentViewsets')

urlpatterns = [
    path('',include(router.urls)),
]


