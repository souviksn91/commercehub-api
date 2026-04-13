from django.urls import path
from .views import CreatePaymentIntentView, stripe_webhook

urlpatterns = [
    path("create-intent/", CreatePaymentIntentView.as_view(), name="create-intent"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),  # add webhook endpoint
]