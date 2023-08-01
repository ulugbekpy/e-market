from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from django.urls import path

from .views import (ProductViewSet,CartViewSet,CartItemViewSet,SelectedAPI)

router = DefaultRouter()

router.register('products',ProductViewSet)
router.register('carts',CartViewSet,basename='cart')

carts_router = NestedDefaultRouter(router,'carts',lookup='cart')
carts_router.register('items',CartItemViewSet,basename='cart-items')

urlpatterns = router.urls + carts_router.urls + \
    [
        path("category/<int:pk>/products/",SelectedAPI.as_view(),name="selected-products")
    ]
