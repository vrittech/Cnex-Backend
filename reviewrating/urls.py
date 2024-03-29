from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.rating_viewsets import RatingViewsets
from .viewsets.apprating_viewsets import AppRatingViewsets

router.register('rate-products',RatingViewsets,basename='RatingViewsets')
router.register('app-rating',AppRatingViewsets,basename='AppRatingViewsets')


urlpatterns = [
    path('',include(router.urls)),
]


