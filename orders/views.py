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

    permission_classes = [IsAuthenticated]

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
class UserOrderListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["status"]
    ordering_fields = ["created_at", "total_price"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

# API endpoint to get details of a specific order for the authenticated user
class UserOrderDetailView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

# API endpoint to list all orders for admin users
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

    permission_classes = [IsAdminUser]

    @extend_schema(
        request=UpdateOrderStatusSerializer
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
