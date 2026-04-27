from rest_framework import serializers
from .models import Order, OrderItem


# serializer for individual order items
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "price", "quantity"]


# serializer for order details (with nested items)
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_price",
            "created_at",
            "items"
        ]