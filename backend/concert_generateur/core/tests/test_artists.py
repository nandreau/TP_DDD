import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from core.models import Artist

User = get_user_model()


@pytest.fixture
def view_artist_permission():
    return Permission.objects.get(codename="view_artist")


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="adminpass", is_staff=True)


@pytest.fixture
def artist_user(db, view_artist_permission):
    user = User.objects.create_user(username="artist", password="artistpass")
    user.user_permissions.add(view_artist_permission)
    return user


@pytest.fixture
def organizer_user(db, view_artist_permission):
    user = User.objects.create_user(username="organizer", password="organizerpass")
    user.user_permissions.add(view_artist_permission)
    return user


@pytest.fixture
def artist_object(db):
    return Artist.objects.create(name="Sia", followers=1000000)


@pytest.fixture
def api_client():
    return APIClient()

# ========== TESTS PUBLICS (lecture seule) ==========

@pytest.mark.django_db
def test_artist_can_view_public_list(api_client, artist_user, artist_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/artists/")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_artist_can_view_artist_detail(api_client, artist_user, artist_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get(f"/api/artists/{artist_object.name}/")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_organizer_cannot_delete_artist(api_client, organizer_user, artist_object):
    api_client.force_authenticate(user=organizer_user)
    response = api_client.delete(f"/api/artists/{artist_object.name}/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ========== TESTS ADMIN ==========

@pytest.mark.django_db
def test_admin_can_delete_artist(api_client, admin_user, artist_object):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f"/api/admin/artists/{artist_object.name}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_non_admin_cannot_access_admin_endpoint(api_client, artist_user, artist_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get(f"/api/admin/artists/{artist_object.name}/")
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]


# ========== TEST DE SÉCURITÉ SUPPLÉMENTAIRE ==========

@pytest.mark.django_db
def test_user_without_permission_gets_403(api_client):
    user = User.objects.create_user(username="noperm", password="nopass")
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/artists/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
