# core/permissions.py
from rest_framework.permissions import BasePermission

class HasPermissions(BasePermission):
    """
    Vérifie que l'utilisateur possède les permissions définies dans l'attribut
    `required_permissions` ou `allowed_roles` de la vue.
    """

    def has_permission(self, request, view):
        perms = getattr(view, 'required_permissions', [])
        logic = getattr(view, 'permission_logic', 'all')
        allowed_roles = getattr(view, 'allowed_roles', [])

        if not request.user or not request.user.is_authenticated:
            return False
        
        if allowed_roles and request.user.role in allowed_roles:
            return True

        if not perms:
            return True

        if logic == 'all':
            return request.user.has_perms(perms)
        elif logic == 'any':
            return any(request.user.has_perm(p) for p in perms)
        return False
