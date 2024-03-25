from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.order_viewsets import OrderViewsets
from .viewsets.order_item_viewsets import OrderItemViewsets
from .viewsets.cart_viewsets import CartViewsets
from .viewsets.wishlist_viewsets import WishlistViewsets
from .viewsets.wishlist import WishlistProductsList
from .viewsets.cart import CartProductsList
# from .viewsets.checkout_viewsets import CheckoutViewsets

router.register('order',OrderViewsets,basename='OrderViewsets')
router.register('order-items',OrderItemViewsets,basename='OrderItemViewsets')
router.register('cart',CartViewsets,basename='CartViewsets')
# router.register('checkout',CheckoutViewsets,basename='CheckoutViewsets')
router.register('wishlist',WishlistViewsets,basename='WishlistViewsets')

urlpatterns = [
    path('',include(router.urls)),
    path('get-wishlist-product/',WishlistProductsList.as_view(),name="WishlistProductsList"),
    # path('get-cart-product/',CartProductsList.as_view(),name="CartProductsList")
]


