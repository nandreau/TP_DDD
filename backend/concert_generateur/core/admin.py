# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models.users import CustomUser
from core.models.countries import Country
from core.models.demographics import CountryDemographics
from core.models.concerthall import ConcertHall

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

# === Admin Country ===
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

# === Admin CountryDemographics ===
@admin.register(CountryDemographics)
class CountryDemographicsAdmin(admin.ModelAdmin):
    list_display = ['country', 'average_cultural_spending_per_capita', 'country_cluster']
    search_fields = ['country__code']
    autocomplete_fields = ['country']

# === Admin ConcertHall ===
@admin.register(ConcertHall)
class ConcertHallAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'capacity', 'country_code']
    search_fields = ['name', 'city', 'country_code']
