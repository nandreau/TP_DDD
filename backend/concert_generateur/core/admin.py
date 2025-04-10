# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models.users import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Affichage dans la liste de l'administration
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']

    # Pour gérer les champs dans le formulaire de changement
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    # Pour la création d'un nouvel utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

    search_fields = ['username', 'email']
    ordering = ['username']

# Enregistrer le modèle avec sa configuration personnalisée
admin.site.register(CustomUser, CustomUserAdmin)
