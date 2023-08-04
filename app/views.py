from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from decimal import Decimal
from typing import List, Dict, Any

from .models import Product, Cart
from .serializers.product import ProductSerializer
from .serializers.cart import CartSerializer, CartItemSerializer
from .pagination import DefaultPagination
from .filters import ProductFilter


# Viewsets
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["title", "description"]
    ordering_fields = ["category", "price", "shop"]


class CartViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return Cart.objects.filter(cart_id=self.kwargs["cart_pk"])


class SelectedAPI(APIView):
    class OutputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.DecimalField(decimal_places=2, max_digits=10)
        amount = serializers.IntegerField()

    def product_list(
        self,
        cat_id,
    ) -> List[Dict[str, Any]]:
        result = []

        products = Product.objects.filter(category=cat_id).all()

        for pro in products:
            pro_info = {
                "title": pro.title,
                "description": pro.description,
                "price": pro.price,
                "amount": pro.amount,
            }
            result.append(pro_info)

        return result

    def get(self, request, pk):
        serializer = self.OutputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        products = self.product_list(cat_id=pk)

        data = self.OutputSerializer(products, many=True).data
        if len(data) > 0:
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Mahsulotlar mavjud emas!"}, status=status.HTTP_204_NO_CONTENT
        )
