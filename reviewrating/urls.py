from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.rating_viewsets import RatingViewsets

router.register('rate-products',RatingViewsets,basename='RatingViewsets')


urlpatterns = [
    path('',include(router.urls)),
]


