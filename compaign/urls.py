from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.faqs_viewsets import FaqsViewsets
from .viewsets.banner_viewsets import BannerViewsets
from .viewsets.privacy_policy_viewsets import PrivacyPolicyViewsets

router.register('faqs',FaqsViewsets,basename='FaqsViewsets')
router.register('banner',BannerViewsets,basename='BannerViewsets')
router.register('privacy-policy',PrivacyPolicyViewsets,basename='PrivacyPolicy')

urlpatterns = [
    path('',include(router.urls)),
]


