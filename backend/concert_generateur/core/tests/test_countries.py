import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from core.models import Country

User = get_user_model()


@pytest.fixture
def view_country_permission():
    return Permission.objects.get(codename="view_country")


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="adminpass", is_staff=True)


@pytest.fixture
def artist_user(db, view_country_permission):
    user = User.objects.create_user(username="artist", password="artistpass")
    user.user_permissions.add(view_country_permission)
    return user


@pytest.fixture
def organizer_user(db, view_country_permission):
    user = User.objects.create_user(username="organizer", password="organizerpass")
    user.user_permissions.add(view_country_permission)
    return user


@pytest.fixture
def country_object(db):
    return Country.objects.create(code="FR", name="France")


@pytest.fixture
def api_client():
    return APIClient()

# ========== TESTS PUBLICS (lecture seule) ==========

@pytest.mark.django_db
def test_artist_can_view_country(api_client, artist_user, country_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/country/FR/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_organizer_can_view_country(api_client, organizer_user, country_object):
    api_client.force_authenticate(user=organizer_user)
    response = api_client.get("/api/country/FR/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_without_permission_gets_403_on_country(api_client, db):
    user = User.objects.create_user(username="noperm", password="pass")
    Country.objects.create(code="DE", name="Germany")
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/country/DE/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


# ========== TESTS ADMIN ==========

@pytest.mark.django_db
def test_admin_can_create_country(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    data = {
        "code": "ES",
        "name": "Spain"
    }
    response = api_client.post("/api/admin/countries/", data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_admin_can_update_country(api_client, admin_user, country_object):
    api_client.force_authenticate(user=admin_user)
    data = {
        "code": "FR",
        "name": "France Métropolitaine"
    }
    response = api_client.put("/api/admin/countries/FR/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "France Métropolitaine"


@pytest.mark.django_db
def test_admin_can_delete_country(api_client, admin_user, country_object):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete("/api/admin/countries/FR/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_non_admin_cannot_access_admin_country_endpoint(api_client, artist_user, country_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/admin/countries/FR/")
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
