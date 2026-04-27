from django.urls import path
from .views import ( 
    CheckoutView,
    UserOrderListView,
    UserOrderDetailView,
    AdminOrderListView,
    UpdateOrderStatusView,
)

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", UserOrderListView.as_view()),
    path("<uuid:pk>/", UserOrderDetailView.as_view()),
    path("admin/", AdminOrderListView.as_view()),
    path("<uuid:pk>/status/", UpdateOrderStatusView.as_view()),    
]