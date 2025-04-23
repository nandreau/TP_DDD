from rest_framework import viewsets
from core.exceptions import handle_api_error
from rest_framework import generics

class BaseSafeModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet admin avec gestion automatique des erreurs API.
    """
    @handle_api_error
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @handle_api_error
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @handle_api_error
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @handle_api_error
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @handle_api_error
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @handle_api_error
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class BaseSafeRetrieveAPIView(generics.RetrieveAPIView):
    """
    Vue read-only sécurisée pour les endpoints publics.
    """
    @handle_api_error
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class BaseSafeListAPIView(generics.ListAPIView):
    """
    Vue read-only pour lister des éléments avec gestion d’erreurs.
    """
    @handle_api_error
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class BaseSafeListCreateAPIView(generics.ListCreateAPIView):
    """
    Vue combinée (GET/POST) sécurisée avec gestion d’erreurs intégrée.
    """
    @handle_api_error
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @handle_api_error
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
