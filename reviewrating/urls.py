from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.review_viewsets import ReviewViewsets
from .viewsets.rating_viewsets import RatingViewsets

router.register('rate-products',RatingViewsets,basename='RatingViewsets')
router.register('review-products',ReviewViewsets,basename='ReviewViewsets')

urlpatterns = [
    path('',include(router.urls)),
]


