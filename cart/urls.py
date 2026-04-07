from django.urls import path
from .views import CartView, AddToCartView, RemoveCartItemView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("remove/<uuid:pk>/", RemoveCartItemView.as_view(), name="remove-cart-item"),
]