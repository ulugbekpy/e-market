from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import (ProductViewSet,CartViewSet,CartItemViewSet)

router = DefaultRouter()

router.register('products',ProductViewSet)
router.register('carts',CartViewSet,basename='cart')

carts_router = NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',CartItemViewSet,basename='cart-items')

urlpatterns = router.urls + carts_router.urls
