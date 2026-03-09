from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        # Using create_user to ensure password is hashed
        user = CustomUser.objects.create_user(  
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user
    
