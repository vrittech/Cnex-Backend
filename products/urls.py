from rest_framework.routers import DefaultRouter
import importlib
from django.urls import path,include

router = DefaultRouter()

from .viewsets.brand_viewsets import BrandViewsets
from .viewsets.category_viewsets import CategoryViewsets
from .viewsets.collection_viewsets import CollectionViewsets
from .viewsets.product_details_after_variations_viewsets import ProductDetailAfterVariationViewsets
from .viewsets.product_have_image_viewsets import ProductHaveImagesViewsets
from .viewsets.prorduct_viewsets import ProductViewsets

router.register('brand',BrandViewsets,basename='BrandViewsets')
router.register('category',CategoryViewsets,basename='CategoryViewsets')
router.register('collection',CollectionViewsets,basename='CollectionViewsets')
router.register('product-detail-after-variation',ProductDetailAfterVariationViewsets,basename='ProductDetailAfterVariationViewsets')
router.register('product-have-images',ProductHaveImagesViewsets,basename='ProductHaveImagesViewsets')
router.register('product-viewsets',ProductViewsets,basename='ProductViewsets')


urlpatterns = [
    path('',include(router.urls)),
]


