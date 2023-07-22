from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet


from django_filters.rest_framework import DjangoFilterBackend

from .models import (Product,Category,Cart)
from .serializers import (ProductSerializer,
                          CategorySerializer,
                          CartSerializer,
                          CartItemSerializer)
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


class CartViewSet(CreateModelMixin,
                  ListModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return Cart.objects.filter(cart_id=self.kwargs['cart_pk'])
