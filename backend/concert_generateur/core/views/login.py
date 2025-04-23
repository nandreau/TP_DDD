from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from core.exceptions import handle_api_error

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    @handle_api_error
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            raise ValueError("Nom d'utilisateur et mot de passe sont requis.")

        user = authenticate(request, username=username, password=password)

        if user is None:
            raise PermissionError("Nom d'utilisateur ou mot de passe invalide.")

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        })
