from rest_framework import serializers
from .models import Order, OrderItem


# serializer for individual order items
class OrderItemSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(
        source="price_at_purchase",
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = OrderItem
        fields = ["id", "product_name", "price", "quantity"]


# serializer for order details (with nested items)
class OrderSerializer(serializers.ModelSerializer):
    
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user_id",
            "user_email",
            "status",
            "total_price",
            "created_at",
            "items"
        ]



class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)