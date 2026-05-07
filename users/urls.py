from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    # path("login/", TokenObtainPairView.as_view(), name="login"),
    # path("refresh/", TokenRefreshView.as_view(), name="refresh"),  
    path(
        "login/",
        extend_schema_view(
            post=extend_schema(
                summary="User Login",
                description="Authenticate a user and return JWT tokens"
            )
        )(TokenObtainPairView).as_view(), 
          name="login"
    ),
    path(
        "refresh/",
        extend_schema_view(
            post=extend_schema(
                summary="Refresh JWT Token",
                description="Generate a new JWT access token using refresh token"
            )
        )(TokenRefreshView).as_view(), 
          name="refresh"
    ),
]