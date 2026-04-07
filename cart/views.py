from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer, AddCartItemSerializer


# helper function to get or create a cart for a user
def get_or_create_cart(user):
    # if user is not authenticated, we cannot create a cart
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# view to retrieve the current user's cart
class CartView(generics.RetrieveAPIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_or_create_cart(self.request.user)


# view to add or update an item in the cart
class AddToCartView(generics.GenericAPIView):

    serializer_class = AddCartItemSerializer
    permission_classes = [IsAuthenticated]

    # handle POST request to add/update cart item
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_or_create_cart(request.user)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        # get or create cart item for this product
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        # if item already exists, update the quantity
        if not created:
            cart_item.quantity += quantity

            # ensure updated quantity does not exceed stock
            if cart_item.quantity > product.inventory.stock:
                return Response(
                    {"error": "Quantity exceeds available stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.save()

        return Response({"message": "Item added to cart"})


# view to remove an item from the cart
class RemoveCartItemView(generics.DestroyAPIView):


    permission_classes = [IsAuthenticated]
    # queryset will be filtered to only include items from the current user's cart
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({"message": "Item removed"})