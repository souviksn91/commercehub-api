from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import create_order_from_cart


# API endpoint to handle checkout process
class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    # POST /api/checkout/ - create an order from the user's cart
    def post(self, request):

        try:
            # create order from cart using the service function
            order = create_order_from_cart(request.user)

            return Response({
                "message": "Order created successfully",
                "order_id": str(order.id)
            })

        except Exception as e:
            # handle errors e.g. cart empty, insufficient stock
            return Response({"error": str(e)}, status=400)