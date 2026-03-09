from rest_framework import generics
from .models import CustomUser
from .serializers import UserRegistrationSerializer


# User registration view
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer