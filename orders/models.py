import uuid
from django.db import models
from django.conf import settings


# represents a user's order
class Order(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("SHIPPED", "Shipped"),
        ("CANCELLED", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"  # allows us to access a user's orders via user.orders.all()
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


# represents individual items inside an order (snapshot of product)
class OrderItem(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # store the product ID for reference, 
    # but we won't link to the product directly since it's a snapshot
    product_id = models.UUIDField()  
    product_name = models.CharField(max_length=255)
    # store the price at the time of purchase for accurate order history
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)  
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"