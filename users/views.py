from rest_framework import generics
from drf_spectacular.utils import extend_schema

from .models import CustomUser
from .serializers import UserRegistrationSerializer



# User registration view
@extend_schema(
    summary="User Registration",
    description="Register a new user with email and password"
)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer