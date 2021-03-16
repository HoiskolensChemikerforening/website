from rest_framework import serializers
from .models import (
    Item,
    ShoppingCart,
    Category,
    Order,
    HappyHour,
    RefillReceipt,
    OrderItem,
)
from chemie.customprofile.serializers import UserSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class HappyHourSerializer(serializers.ModelSerializer):
    provider = UserSerializer()

    class Meta:
        model = HappyHour
        fields = "__all__"


class RefillReceiptSerializer(serializers.ModelSerializer):
    provider = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = RefillReceipt
        fields = "__all__"
