# core/permissions.py
from rest_framework.permissions import BasePermission

class HasPermissions(BasePermission):
    """
    Vérifie que l'utilisateur possède les permissions définies dans l'attribut
    `required_permissions` de la vue.

    Tu peux définir en plus l'attribut `permission_logic` dans la vue :
      - "all" (par défaut) : L'utilisateur doit avoir TOUTES les permissions listées.
      - "any" : L'utilisateur doit avoir AU MOINS UNE des permissions listées.
    """
    def has_permission(self, request, view):
        perms = getattr(view, 'required_permissions', [])
        logic = getattr(view, 'permission_logic', 'all')
        if not request.user or not request.user.is_authenticated:
            return False

        # Si aucune permission n'est spécifiée, autorise par défaut
        if not perms:
            return True

        if logic == 'all':
            return request.user.has_perms(perms)
        elif logic == 'any':
            return any(request.user.has_perm(perm) for perm in perms)
        else:
            # Si on donne un mode non reconnu, refuse l'accès
            return False
