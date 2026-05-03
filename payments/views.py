import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import metadata, status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema

from orders.models import Order
from .serializers import CreatePaymentIntentSerializer



# set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


# creates a Stripe PaymentIntent for an order
class CreatePaymentIntentView(APIView):

    permission_classes = [IsAuthenticated]
    # define the expected input for this endpoint 
    @extend_schema(
        request=CreatePaymentIntentSerializer
    )

    def post(self, request):

        serializer = CreatePaymentIntentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data["order_id"]

        try:
            # fetch the order and ensure it belongs to the authenticated user
            order = Order.objects.get(id=order_id, user=request.user)

            # prevent duplicate payment intents for the same order
            if order.status == "PAID":
                return Response(
                    {"error": "Order is already paid"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # ensure order has items 
            if not order.items.exists():
                return Response(
                    {"error": "Order has no items"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            
            # convert price to smallest currency unit (paise for INR)
            amount = int(order.total_price * 100)

            # create a Stripe PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="inr",
                metadata={
                    "order_id": str(order.id)
                }
            )

            # return the client secret to the frontend to complete the payment
            return Response({
                "client_secret": intent.client_secret
            })
        
        # handle cases where order does not exist or does not belong to user
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        





# Stripe webhook endpoint to handle payment events (e.g. payment success)
@csrf_exempt
def stripe_webhook(request):

    # retrieve the request's body and Stripe signature header to verify the webhook
    payload = request.body  
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        # verify webhook signature and construct the event object
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

    # handle invalid signature error
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)


    # handle the payment_intent.succeeded event to update order status to PAID
    if event["type"] == "payment_intent.succeeded":

        intent = event["data"]["object"]  # the PaymentIntent object

        # extract order_id from the PaymentIntent's metadata (set when creating the intent)
        # metadata = dict(intent.metadata) if intent.metadata else {} 
        order_id = intent.metadata["order_id"] if "order_id" in intent.metadata else None

        if not order_id:
            print("No order_id in metadata — skipping")  # debug statement
            return HttpResponse(status=200)  # ignore silently

        # update the corresponding order's status to PAID in the database
        try:
            order = Order.objects.get(id=order_id)
            order.status = "PAID"
            order.save()
            
            print(f"Order {order_id} marked as PAID")  # debug statement


        except Order.DoesNotExist:
            print("Order not found")  # debug statement

    return HttpResponse(status=200)