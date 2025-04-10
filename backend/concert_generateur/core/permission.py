# core/permissions.py
from rest_framework.permissions import BasePermission

class CanViewDashboardPermission(BasePermission):
    """
    Permission personnalisée qui vérifie si l'utilisateur dispose de la permission 'core.can_view_dashboard'.
    """
    def has_permission(self, request, view):
        # Vérifiez que l'utilisateur est authentifié et qu'il possède la permission
        return request.user and request.user.is_authenticated and request.user.has_perm('core.can_view_dashboard')
