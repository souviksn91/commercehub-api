from rest_framework import serializers
from .models import Product, Category


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

    stock = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "category",
            "is_active",
            "stock"
        ]

    def create(self, validated_data):
        stock = validated_data.pop("stock", 0)
        product = Product.objects.create(**validated_data)
        # create inventory with initial stock
        product.inventory.stock = stock
        product.inventory.save()
        return product
    
    def update(self, instance, validated_data):
        stock = validated_data.pop("stock", None)
        instance = super().update(instance, validated_data)

        if stock is not None:
            instance.inventory.stock = stock
            instance.inventory.save()
        return instance



# used for category read/write operations
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "created_at"]