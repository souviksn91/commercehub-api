from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = ["category__slug"]

    search_fields = ["name", "description"]


class ProductDetailView(generics.RetrieveAPIView):

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer