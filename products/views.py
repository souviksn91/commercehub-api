from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema

from .models import Product, Category
from .serializers import ProductWriteSerializer, ProductReadSerializer, CategorySerializer


# product lisitng view (for all users)
@extend_schema(
    summary="List products",
    description="Retrieve a list of active products with optional filtering by category, search, and ordering",
)
class ProductListView(generics.ListAPIView):
    
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductReadSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category__slug"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "price"]
    ordering = ["-created_at"]


# product detail view (for all users)
@extend_schema(
    summary="Get product details",
    description="Retrieve detailed information about a specific active product by its ID",
)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductReadSerializer


# create a product (only by admin)
@extend_schema(
    summary="Create product",
    description="Create a new product (admin only)",
)
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAdminUser]


# update a product (only by admin)
@extend_schema(
    summary="Update product",
    description="Update an existing product (admin only)",
)
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAdminUser]


# delete a product (only by admin)
@extend_schema(
    summary="Delete product",
    description="Delete an existing product (admin only)",
)
class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWriteSerializer
    permission_classes = [IsAdminUser]


# category list for public 
@extend_schema(
    summary="List categories",
    description="Retrieve a list of all categories",
)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



# create a category for admin
@extend_schema(
    summary="Create category",
    description="Create a new category (admin only)",
)
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]



# update category for admin
@extend_schema(
    summary="Update category",
    description="Update an existing category (admin only)",
)
class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]



# delete category for admin
@extend_schema(
    summary="Delete category",
    description="Delete an existing category (admin only)",
)
class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]