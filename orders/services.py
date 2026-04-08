from django.db import transaction
from decimal import Decimal

from cart.models import Cart
from .models import Order, OrderItem


# service function to create an order from a user's cart
def create_order_from_cart(user):

    # use a transaction to ensure data integrity in case of errors (e.g. insufficient stock)
    with transaction.atomic():  # atomic ensures that a set of database operations are treated as a single (all-or-nothing) unit

        cart = Cart.objects.select_for_update().get(user=user)

        if not cart.items.exists():
            raise Exception("Cart is empty")

        total_price = Decimal("0.00")

        # create the order with a placeholder total price 
        order = Order.objects.create(user=user, total_price=0)

        for item in cart.items.select_related("product"):
            product = item.product
            # lock the inventory record for this product
            inventory = product.inventory.__class__.objects.select_for_update().get(product=product)  

            if item.quantity > inventory.stock:
                raise Exception(f"Not enough stock for {product.name}")

            # deduct stock
            inventory.stock -= item.quantity
            inventory.save()

            # calculate total price
            total_price += product.price * item.quantity

            # create order item snapshot
            OrderItem.objects.create(
                order=order,
                product_id=product.id,
                product_name=product.name,
                price_at_purchase=product.price,
                quantity=item.quantity,
            )

        # update total price
        order.total_price = total_price
        order.save()

        # clear cart
        cart.items.all().delete()

        return order