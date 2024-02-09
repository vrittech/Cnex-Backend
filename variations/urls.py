from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.variation_viewsets import VariationViewsets
from .viewsets.variation_option_viewsets import VariationOptionViewsets
from .viewsets.variation_group_viewsets import VariationGroupViewsets

router.register('variations',VariationViewsets,basename='VariationViewsets')
router.register('variations-options',VariationOptionViewsets,basename='VariationOptionViewsets')
router.register('variations-groups',VariationGroupViewsets,basename='VariationGroupViewsets')

urlpatterns = [
    path('',include(router.urls)),
]


