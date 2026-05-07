from rest_framework import generics
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .services import create_order_from_cart
from .models import Order
from .serializers import OrderSerializer, UpdateOrderStatusSerializer


# API endpoint to handle checkout process
class CheckoutView(APIView):

    serializer_class = None  # serializer added for swagger documentation
    permission_classes = [IsAuthenticated]

    # swagger documentation for this endpoint
    @extend_schema(
        summary="Checkout and create order",
        description="Create an order from the user's cart and clear the cart after successful order creation",
    )

    # POST /api/checkout/ - create an order from the user's cart
    def post(self, request):

        try:
            # create order from cart using the service function
            order = create_order_from_cart(request.user)

            # clear the cart after creating the order
            cart = request.user.cart
            cart.items.all().delete() 

            return Response({
                "message": "Order created successfully",
                "order_id": str(order.id)
            })

        except Exception as e:
            # handle errors e.g. cart empty, insufficient stock
            return Response({"error": str(e)}, status=400)
        


# API endpoint to list all orders for the authenticated user
@extend_schema(
    summary="List user orders",
    description="Retrieve a list of orders for the authenticated user",
)
class UserOrderListView(generics.ListAPIView):

    queryset = Order.objects.none()  # empty queryset added for swagger documentation
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status"]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

# API endpoint to get details of a specific order for the authenticated user
@extend_schema(
    summary="Get order details",
    description="Retrieve details of a specific order for the authenticated user",
)
class UserOrderDetailView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

# API endpoint to list all orders for admin users
@extend_schema(
    summary="List all orders (admin)",
    description="Admin endpoint to retrieve all orders with filtering, search, and ordering capabilities",
)
class AdminOrderListView(generics.ListAPIView):

    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["status"]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]

    search_fields = ["user__email"]

    def get_queryset(self):
        return Order.objects.all()


# API endpoint to update order status (admin only)
class UpdateOrderStatusView(APIView):

    serializer_class = UpdateOrderStatusSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        request=UpdateOrderStatusSerializer,
        summary="Update order status (admin)",
        description="Update the status of an order (PENDING, PAID, SHIPPED, CANCELLED)",
    )

    def patch(self, request, pk):

        serializer = UpdateOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = Order.objects.get(id=pk)

            order.status = serializer.validated_data["status"]
            order.save()

            return Response({"message": "Order status updated"})

        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
