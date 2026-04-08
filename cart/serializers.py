from rest_framework import serializers

from .models import Cart, CartItem
from products.models import Product


# serializer for CartItem (used inside Cart response)
class CartItemSerializer(serializers.ModelSerializer):

    # include product name and price for convenience
    product_name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_name", "price", "quantity"]


# serializer for full Cart view
class CartSerializer(serializers.ModelSerializer):

    # nested items using CartItemSerializer
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items"]


# serializer for adding/updating items in cart
class AddCartItemSerializer(serializers.Serializer):
    
    # only need product_id and quantity for adding/updating items
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

    # validate product existence and active status
    def validate(self, data):
        # validate product existence
        try:
            product = Product.objects.get(id=data["product_id"])
        # handle case where product does not exist
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        # validate product is active
        if not product.is_active:
            raise serializers.ValidationError("Product is not active")
        # validate stock availability
        if data["quantity"] > product.inventory.stock:
            raise serializers.ValidationError("Not enough stock available")
        
        # if validation passes, include the product instance in validated data for use in view
        data["product"] = product
        return data
    

# serializer for updating cart item quantity
class UpdateCartItemSerializer(serializers.Serializer):

    quantity = serializers.IntegerField(min_value=0)