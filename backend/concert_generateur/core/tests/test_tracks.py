import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Track, Artist
from django.contrib.auth.models import Permission
from datetime import date

User = get_user_model()

@pytest.fixture
def permissions():
    return {
        "view": Permission.objects.get(codename="view_track"),
    }

@pytest.fixture
def artist_user(db, permissions):
    user = User.objects.create_user(username="artist", password="artistpass", role="artist")
    user.user_permissions.add(permissions["view"])
    return user

@pytest.fixture
def organizer_user(db, permissions):
    user = User.objects.create_user(username="organizer", password="organizerpass", role="organizer")
    user.user_permissions.add(permissions["view"])
    return user

@pytest.fixture
def artist_object(db):
    return Artist.objects.create(name="Sia", followers=2000000)

@pytest.fixture
def track_object(db, artist_object):
    return Track.objects.create(
        title="Chandelier",
        artist=artist_object,
        release_date=date(2014, 3, 17),
        streams=500000000
    )

@pytest.fixture
def api_client():
    return APIClient()

# ========== PUBLIC TRACK ACCESS ==========

@pytest.mark.django_db
def test_artist_can_list_tracks(api_client, artist_user, track_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/tracks/")
    assert response.status_code == status.HTTP_200_OK
    assert any(t["title"] == "Chandelier" for t in response.data["results"])

@pytest.mark.django_db
def test_organizer_can_list_tracks(api_client, organizer_user, track_object):
    api_client.force_authenticate(user=organizer_user)
    response = api_client.get("/api/tracks/")
    assert response.status_code == status.HTTP_200_OK
    assert any(t["title"] == "Chandelier" for t in response.data["results"])

@pytest.mark.django_db
def test_artist_can_see_track_detail(api_client, artist_user, track_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get(f"/api/tracks/{track_object.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Chandelier"

@pytest.mark.django_db
def test_track_by_artist_returns_results(api_client, artist_user, track_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/tracks/by-artist/Sia/")
    assert response.status_code == status.HTTP_200_OK
    assert any(t["title"] == "Chandelier" for t in response.data["results"])

@pytest.mark.django_db
def test_artist_cannot_delete_track(api_client, artist_user, track_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.delete(f"/api/tracks/{track_object.id}/")
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED]
