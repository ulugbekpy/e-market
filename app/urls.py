from rest_framework.routers import DefaultRouter

from .views import (ProductViewSet,UserViewSet)

router = DefaultRouter()

router.register('products',ProductViewSet)
router.register('users',UserViewSet)

urlpatterns = router.urls
