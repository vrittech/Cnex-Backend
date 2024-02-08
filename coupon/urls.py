from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.coupon_viewsets import CouponViewsets

router.register('coupon',CouponViewsets,basename='CouponViewsets')

urlpatterns = [
    path('',include(router.urls)),
]


