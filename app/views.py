from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet


from django_filters.rest_framework import DjangoFilterBackend

from .models import (Product,Category,Cart)
from .serializers import (ProductSerializer,CategorySerializer,CartSerializer)
from .pagination import DefaultPagination
from .filters import ProductFilter


# Viewsets
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['category', 'price', 'shop']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(CreateModelMixin,ListModelMixin,GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer