import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from core.models import ConcertHall

User = get_user_model()


@pytest.fixture
def view_concerthall_permission():
    return Permission.objects.get(codename="view_concerthall")


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="adminpass", is_staff=True)


@pytest.fixture
def artist_user(db, view_concerthall_permission):
    user = User.objects.create_user(username="artist", password="artistpass")
    user.user_permissions.add(view_concerthall_permission)
    return user


@pytest.fixture
def organizer_user(db, view_concerthall_permission):
    user = User.objects.create_user(username="organizer", password="organizerpass")
    user.user_permissions.add(view_concerthall_permission)
    return user


@pytest.fixture
def concerthall_object(db):
    return ConcertHall.objects.create(
        name="Accor Arena",
        city="Paris",
        country_code="FR",
        capacity=20000
    )


@pytest.fixture
def api_client():
    return APIClient()

# ========== TESTS PUBLICS (lecture seule) ==========

@pytest.mark.django_db
def test_artist_can_list_concerthalls(api_client, artist_user, concerthall_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/concerthalls/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_artist_can_retrieve_concerthall(api_client, artist_user, concerthall_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get(f"/api/concerthalls/{concerthall_object.id}/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_organizer_can_list_concerthalls_by_country(api_client, organizer_user, concerthall_object):
    api_client.force_authenticate(user=organizer_user)
    response = api_client.get("/api/concerthalls/by-country/FR/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_artist_cannot_delete_concerthall(api_client, artist_user, concerthall_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.delete(f"/api/concerthalls/{concerthall_object.id}/")
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED]


# ========== TESTS ADMIN ==========

@pytest.mark.django_db
def test_admin_can_delete_concerthall(api_client, admin_user, concerthall_object):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f"/api/admin/concerthalls/{concerthall_object.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_admin_can_create_concerthall(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    data = {
        "name": "Stade Pierre-Mauroy",
        "city": "Lille",
        "country_code": "FR",
        "capacity": 25000
    }
    response = api_client.post("/api/admin/concerthalls/", data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_non_admin_cannot_access_admin_endpoint(api_client, artist_user, concerthall_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get(f"/api/admin/concerthalls/{concerthall_object.id}/")
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]


# ========== TEST DE SÉCURITÉ ==========

@pytest.mark.django_db
def test_user_without_permission_gets_403_on_public_concerthalls(api_client):
    user = User.objects.create_user(username="no_perm", password="pass")
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/concerthalls/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
