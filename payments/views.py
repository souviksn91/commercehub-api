import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from orders.models import Order



# set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


# creates a Stripe PaymentIntent for an order
class CreatePaymentIntentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")

        try:
            # fetch the order and ensure it belongs to the authenticated user
            order = Order.objects.get(id=order_id, user=request.user)

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
        order_id = intent["metadata"]["order_id"]  # retrieve order ID from metadata

        # update the corresponding order's status to PAID in the database
        try:
            order = Order.objects.get(id=order_id)
            order.status = "PAID"
            order.save()

        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)