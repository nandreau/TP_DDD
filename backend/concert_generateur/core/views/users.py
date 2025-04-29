from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from core.models.users import CustomUser
from core.serializers.users import UserRegistrationSerializer, UserSerializer
from core.views.base import BaseSafeListCreateAPIView, BaseSafeModelViewSet, BaseSafeRetrieveUpdateAPIView

class UserRegistrationView(BaseSafeListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserAdminViewSet(BaseSafeModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserProfileView(BaseSafeRetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
