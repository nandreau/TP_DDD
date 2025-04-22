import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    return user

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username="user", password="userpass")

@pytest.fixture
def group_object(db):
    return Group.objects.create(name="Musiciens")

@pytest.fixture
def api_client():
    return APIClient()

# ========== ADMIN ACCESS ==========

@pytest.mark.django_db
def test_admin_can_list_groups(api_client, admin_user, group_object):
    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/admin/groups/")
    results = response.data["results"] if "results" in response.data else response.data
    assert any(g["name"] == "Musiciens" for g in results)


@pytest.mark.django_db
def test_admin_can_create_group(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post("/api/admin/groups/", {"name": "Producteurs"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Producteurs"

@pytest.mark.django_db
def test_admin_can_update_group(api_client, admin_user, group_object):
    api_client.force_authenticate(user=admin_user)
    url = f"/api/admin/groups/{group_object.id}/"
    response = api_client.patch(url, {"name": "Compositrices"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Compositrices"

@pytest.mark.django_db
def test_admin_can_delete_group(api_client, admin_user, group_object):
    api_client.force_authenticate(user=admin_user)
    url = f"/api/admin/groups/{group_object.id}/"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

# ========== NON-ADMIN ACCESS ==========

@pytest.mark.django_db
def test_non_admin_cannot_list_groups(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    response = api_client.get("/api/admin/groups/")
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_non_admin_cannot_create_group(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    response = api_client.post("/api/admin/groups/", {"name": "Interdits"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
