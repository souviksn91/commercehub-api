from django.urls import path
from .views import CartView, AddToCartView, RemoveCartItemView, UpdateCartItemView

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path("remove/<uuid:pk>/", RemoveCartItemView.as_view(), name="remove-cart-item"),
    path("items/<uuid:pk>/", UpdateCartItemView.as_view(), name="update-cart-item"),
]