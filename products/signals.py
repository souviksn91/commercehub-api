from django.db.models.signals import post_save  # to trigger actions after saving a model instance
from django.dispatch import receiver  # decorator to connect signals to receiver functions

from .models import Product, Inventory


@receiver(post_save, sender=Product)  # listen for the post_save signal from the Product model
def create_inventory(sender, instance, created, **kwargs):

    # if a new product is created, automatically create an inventory record for it with default stock of 0
    if created:
        Inventory.objects.create(product=instance)