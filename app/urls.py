from rest_framework.routers import DefaultRouter

from .views import (ProductViewSet,CategoryViewSet,CartViewSet)

router = DefaultRouter()

router.register('products',ProductViewSet)
router.register('categories',CategoryViewSet)
router.register('carts',CartViewSet)

urlpatterns = router.urls
