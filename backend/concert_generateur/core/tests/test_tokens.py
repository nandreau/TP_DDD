import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    return user

@pytest.fixture
def artist_user(db):
    return User.objects.create_user(username="artist", password="artistpass")

@pytest.fixture
def token_for_artist(artist_user):
    return Token.objects.create(user=artist_user)

@pytest.fixture
def api_client():
    return APIClient()

# ========== GET (liste des tokens) ==========

@pytest.mark.django_db
def test_admin_can_list_tokens(api_client, admin_user, token_for_artist):
    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/token-proxy/")
    assert response.status_code == status.HTTP_200_OK
    assert any(entry["user"] == "artist" for entry in response.data)

@pytest.mark.django_db
def test_non_admin_cannot_list_tokens(api_client, artist_user):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/token-proxy/")
    assert response.status_code == status.HTTP_403_FORBIDDEN

# ========== POST (génération ou récupération) ==========

@pytest.mark.django_db
def test_admin_can_create_token_for_user(api_client, admin_user, artist_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post("/api/token-proxy/", {"username": "artist"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "artist"
    assert "token" in response.data

@pytest.mark.django_db
def test_post_without_username_returns_400(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post("/api/token-proxy/", {})  # No username
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_post_with_unknown_user_returns_404(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post("/api/token-proxy/", {"username": "unknownuser"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
