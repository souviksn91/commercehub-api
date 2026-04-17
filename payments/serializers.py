from rest_framework import serializers


# serializer for creating a payment intent
class CreatePaymentIntentSerializer(serializers.Serializer):

    order_id = serializers.UUIDField()