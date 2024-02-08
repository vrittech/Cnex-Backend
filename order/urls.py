from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.order_viewsets import OrderViewsets
from .viewsets.order_item_viewsets import OrderItemViewsets
from .viewsets.cart_viewsets import CartViewsets
from .viewsets.wishlist_viewsets import WishlistViewsets

router.register('order',OrderViewsets,basename='OrderViewsets')
router.register('order-items',OrderItemViewsets,basename='OrderItemViewsets')
router.register('cart',CartViewsets,basename='CartViewsets')
router.register('wishlist',WishlistViewsets,basename='WishlistViewsets')

urlpatterns = [
    path('',include(router.urls)),
]


