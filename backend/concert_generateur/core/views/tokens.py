from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class TokenProxyView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # Liste tous les tokens existants pour les utilisateurs
        tokens = Token.objects.all()
        data = [{"user": token.user.username, "token": token.key} for token in tokens]
        return Response(data)

    def post(self, request, format=None):
        # Crée ou récupère le token pour un utilisateur donné
        username = request.data.get("username")
        if not username:
            return Response({"detail": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"username": user.username, "token": token.key}, status=status.HTTP_200_OK)
