import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Genre, GenreFamily
from django.contrib.auth.models import Permission

User = get_user_model()

@pytest.fixture
def genre_family(db):
    return GenreFamily.objects.create(name="Pop/Rock")

@pytest.fixture
def genre(db, genre_family):
    return Genre.objects.create(name="Pop", family=genre_family)

@pytest.fixture
def artist_user(db):
    user = User.objects.create_user(username="artist", password="artistpass", role="artist")
    perm = Permission.objects.get(codename="view_genre")
    user.user_permissions.add(perm)
    return user

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="adminpass", is_staff=True)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_artist_can_list_genres(api_client, artist_user, genre):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/genres/")
    assert response.status_code == status.HTTP_200_OK
    assert any(g["name"] == "Pop" for g in response.data["results"])

@pytest.mark.django_db
def test_admin_can_create_genre(api_client, admin_user, genre_family):
    api_client.force_authenticate(user=admin_user)
    data = {
        "name": "Electro",
        "family": genre_family.id
    }
    response = api_client.post("/api/admin/genres/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Electro"
