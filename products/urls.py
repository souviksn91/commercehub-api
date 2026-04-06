from django.urls import path
from .views import (
    ProductListView, 
    ProductDetailView, 
    ProductCreateView, 
    ProductUpdateView, 
    ProductDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

urlpatterns = [
    # for users
    path("", ProductListView.as_view(), name="product-list"),
    path("<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("categories/", CategoryListView.as_view(), name="category-list"),

    # for admin
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path("<uuid:pk>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("<uuid:pk>/delete/", ProductDeleteView.as_view(), name="product-delete"),
    path("categories/create/", CategoryCreateView.as_view(), name="category-create"),
    path("categories/<uuid:pk>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("categories/<uuid:pk>/delete/", CategoryDeleteView.as_view(), name="category-delete"),

]