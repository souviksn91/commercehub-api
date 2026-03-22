from rest_framework import serializers
from .models import Product



class ProductSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()
    # automatically returns inventory stock
    stock = serializers.IntegerField(source="inventory.stock", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "stock",
            "is_active",
            "created_at",
        ]