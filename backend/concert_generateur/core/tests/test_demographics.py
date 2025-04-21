import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from core.models import Country, CountryDemographics

User = get_user_model()


@pytest.fixture
def view_demographics_permission():
    return Permission.objects.get(codename="view_countrydemographics")


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="adminpass", is_staff=True)


@pytest.fixture
def artist_user(db, view_demographics_permission):
    user = User.objects.create_user(username="artist", password="artistpass")
    user.user_permissions.add(view_demographics_permission)
    return user


@pytest.fixture
def organizer_user(db, view_demographics_permission):
    user = User.objects.create_user(username="organizer", password="organizerpass")
    user.user_permissions.add(view_demographics_permission)
    return user


@pytest.fixture
def country_object(db):
    return Country.objects.create(code="FR", name="France")


@pytest.fixture
def demographics_object(db, country_object):
    return CountryDemographics.objects.create(
        country=country_object,
        average_online_ticket_purchase_rate=0.42,
        average_concert_participation_rate=0.63,
        annual_average_cultural_spending_per_capita=500.0
    )


@pytest.fixture
def api_client():
    return APIClient()


# ========== TESTS PUBLICS (lecture seule) ==========

@pytest.mark.django_db
def test_artist_can_view_demographics(api_client, artist_user, demographics_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/demographics/FR/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_organizer_can_view_demographics(api_client, organizer_user, demographics_object):
    api_client.force_authenticate(user=organizer_user)
    response = api_client.get("/api/demographics/FR/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_without_permission_gets_403(api_client, country_object):
    user = User.objects.create_user(username="noperm", password="1234")
    CountryDemographics.objects.create(country=country_object)
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/demographics/FR/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_post_on_readonly_endpoint_returns_405(api_client, artist_user, country_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.post("/api/demographics/FR/", data={})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


# ========== TESTS ADMIN (CRUD) ==========

@pytest.mark.django_db
def test_admin_can_create_demographics(api_client, admin_user, country_object):
    api_client.force_authenticate(user=admin_user)
    data = {
        "country": country_object.code,
        "average_online_ticket_purchase_rate": 0.4,
        "annual_average_cultural_spending_per_capita": 300.0
    }
    response = api_client.post("/api/admin/demographics/", data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_admin_can_update_demographics(api_client, admin_user, demographics_object):
    api_client.force_authenticate(user=admin_user)
    url = f"/api/admin/demographics/{demographics_object.country.code}/"
    data = {
        "country": "FR",
        "average_online_ticket_purchase_rate": 0.8,
        "annual_average_cultural_spending_per_capita": 999.9
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_online_ticket_purchase_rate"] == 0.8


@pytest.mark.django_db
def test_admin_can_delete_demographics(api_client, admin_user, demographics_object):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f"/api/admin/demographics/{demographics_object.country.code}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_non_admin_cannot_access_admin_endpoint(api_client, artist_user, demographics_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get(f"/api/admin/demographics/{demographics_object.country.code}/")
    assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]
