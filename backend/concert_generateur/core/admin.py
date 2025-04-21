# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models.users import CustomUser
from core.models.countries import Country
from core.models.demographics import CountryDemographics
from core.models.concerthall import ConcertHall
from core.models.event import Event
from core.models.genres import Genre, GenreFamily
from core.models.artists import Artist
from core.models.tracks import Track

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

    search_fields = ['username', 'email']
    ordering = ['username']


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

# === Admin Event ===
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_start', 'event_end', 'concert_hall']
    search_fields = ['title']
    list_filter = ['concert_hall']
    autocomplete_fields = ['concert_hall']

# === Admin Genre ===
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'family']
    search_fields = ['name']
    list_filter = ['family']
    autocomplete_fields = ['family']

# === Admin GenreFamily ===
@admin.register(GenreFamily)
class GenreFamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'age_group_streams']
    search_fields = ['name']

# === Admin Artist ===
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'genre', 'genre_family', 'followers', 'spotify_popularity', 'longevity', 'top_chart_presence', 'spotify_streams_total']
    search_fields = ['name']
    list_filter = ['genre', 'genre_family']

# === Admin Track ===
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date', 'entry_date', 'entry_rank', 'current_rank', 'peak_rank', 'peak_date', 'appearances', 'consecutive_appearances', 'streams', 'source_date']
    search_fields = ['name']
    list_filter = ['artist']
    autocomplete_fields = ['artist']
