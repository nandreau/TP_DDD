import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="adminpass", is_staff=True, role="admin")

@pytest.fixture
def artist_user(db):
    return User.objects.create_user(username="artist", password="artistpass", role="artist")

@pytest.fixture
def api_client():
    return APIClient()

# ========== /register/ ==========

@pytest.mark.django_db
def test_user_can_register(api_client):
    data = {
        "username": "newuser",
        "password": "newpass123",
        "email": "newuser@example.com",
        "role": "artist"
    }
    response = api_client.post("/api/register/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"

# ========== /profile/ ==========

@pytest.mark.django_db
def test_artist_can_view_own_profile(api_client, artist_user):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/profile/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "artist"

@pytest.mark.django_db
def test_artist_can_update_own_profile(api_client, artist_user):
    api_client.force_authenticate(user=artist_user)
    response = api_client.patch("/api/profile/", {"email": "artist@newmail.com"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == "artist@newmail.com"

# ========== /admin/users/ ==========

@pytest.mark.django_db
def test_admin_can_list_users(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/admin/users/")
    assert response.status_code == status.HTTP_200_OK
    assert any("username" in user for user in response.data["results"])

@pytest.mark.django_db
def test_non_admin_cannot_access_user_list(api_client, artist_user):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/admin/users/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
