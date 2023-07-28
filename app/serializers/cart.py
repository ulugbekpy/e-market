from rest_framework import serializers
from models import Cart,CartItem,Shop,Product

class SimpleShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name']


class SimpleProductSerializer(serializers.ModelSerializer):
    shop = SimpleShopSerializer()
    class Meta:
        model = Product
        fields = ['title','price','shop']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity*cart_item.product.price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total = serializers.SerializerMethodField()

    def get_total(self,cart):
        return sum([item.quantity*item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id','ip_address','items','total']