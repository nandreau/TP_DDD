from rest_framework import generics
from rest_framework.permissions import AllowAny
from core.models.users import CustomUser
from core.serializers.users import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
