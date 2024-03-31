from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.faqs_viewsets import FaqsViewsets
from .viewsets.banner_viewsets import BannerViewsets
from .viewsets.privacy_policy_viewsets import PrivacyPolicyViewsets
from .viewsets.term_and_condition_viewsets import TermAndConditionViewsets
from .viewsets.help_and_support_viewsets import HelpAndSupportViewsets

router.register('faqs',FaqsViewsets,basename='FaqsViewsets')
router.register('banner',BannerViewsets,basename='BannerViewsets')
router.register('privacy-policy',PrivacyPolicyViewsets,basename='PrivacyPolicy')

router.register('term-and-condition',TermAndConditionViewsets,basename='TermAndConditionViewsets')
router.register('help-and-support',HelpAndSupportViewsets,basename='HelpAndSupportViewsets')

urlpatterns = [
    path('',include(router.urls)),
]


