from rest_framework import serializers
from .models import Product


# used for reading data
class ProductReadSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()
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

# used for creating/updating data (no id, stock, created_at)
class ProductWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "category",
            "is_active",
        ]