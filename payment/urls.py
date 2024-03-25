from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include
from .viewsets.payment_viewsets import PaymentViewsets
from .viewsets.verify_payment import PaymentVerify


router = DefaultRouter()

router.register('payment',PaymentViewsets,basename='PaymentViewsets')

urlpatterns = [
    path('',include(router.urls)),
    path('payment-verify',PaymentVerify.as_view(),name="PaymentVerify")
    # path('get-wishlist-product/',WishlistProductsList.as_view(),name="WishlistProductsList"),s
]