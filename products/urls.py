from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

urlpatterns = [
    # for users
    path("", ProductListView.as_view(), name="product-list"),
    path("<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    # for admin
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path("<uuid:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("<uuid:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),

]