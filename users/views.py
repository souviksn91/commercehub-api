from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import CustomUser
from .serializers import UserRegistrationSerializer
from .throttles import LoginRateThrottle, RegisterRateThrottle



# user registration view
@extend_schema(
    summary="User Registration",
    description="Register a new user with email and password"
)
class RegisterView(generics.CreateAPIView):
    throttle_classes = [RegisterRateThrottle]  # apply registration throttle
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer



# custom JWT login view with rate limiting
class LoginView(TokenObtainPairView):

    # apply rate limiting to login endpoint
    throttle_classes = [LoginRateThrottle]