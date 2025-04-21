import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from core.models import Event, ConcertHall

from datetime import datetime, timedelta
from django.utils.timezone import make_aware

User = get_user_model()

@pytest.fixture
def permissions():
    return {
        "view": Permission.objects.get(codename="view_event"),
        "add": Permission.objects.get(codename="add_event"),
        "change": Permission.objects.get(codename="change_event"),
    }

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username="admin", password="adminpass", is_staff=True)
    perm = Permission.objects.get(codename="change_event")
    user.user_permissions.add(perm)
    return user


@pytest.fixture
def artist_user(db, permissions):
    user = User.objects.create_user(username="artist", password="artistpass", role="artist")
    user.user_permissions.add(permissions["view"])
    return user

@pytest.fixture
def organizer_user(db, permissions):
    user = User.objects.create_user(username="organizer", password="organizerpass", role="organizer")
    user.user_permissions.add(permissions["view"], permissions["add"], permissions["change"])
    return user

@pytest.fixture
def concert_hall(db):
    return ConcertHall.objects.create(name="Olympia", city="Paris", country_code="FR", capacity=5000)

@pytest.fixture
def event_object(db, concert_hall, artist_user, organizer_user):
    event = Event.objects.create(
        title="Paris Live",
        event_start=make_aware(datetime.now() + timedelta(days=1)),
        event_end=make_aware(datetime.now() + timedelta(days=2)),
        concert_hall=concert_hall,
        organizer=organizer_user
    )
    event.artists.add(artist_user)
    return event

@pytest.fixture
def api_client():
    return APIClient()

# ======= PUBLIC ACCESS (lecture seule) =======

@pytest.mark.django_db
def test_artist_can_see_own_events(api_client, artist_user, event_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/events/")
    assert response.status_code == status.HTTP_200_OK
    events = response.data["results"] if "results" in response.data else response.data
    assert any(event["title"] == "Paris Live" for event in events)


@pytest.mark.django_db
def test_organizer_can_see_all_events(api_client, organizer_user, event_object):
    api_client.force_authenticate(user=organizer_user)
    response = api_client.get("/api/events/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_artist_event_detail(api_client, artist_user, event_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get(f"/api/events/{event_object.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Paris Live"

@pytest.mark.django_db
def test_artist_can_filter_by_country(api_client, artist_user, event_object):
    api_client.force_authenticate(user=artist_user)
    response = api_client.get("/api/events/by-country/FR/")
    assert response.status_code == status.HTTP_200_OK

# ======= ORGANIZER CREATE / UPDATE =======

@pytest.mark.django_db
def test_organizer_can_create_event(api_client, organizer_user, concert_hall):
    api_client.force_authenticate(user=organizer_user)
    data = {
        "title": "Nouveau Concert",
        "event_start": make_aware(datetime.now() + timedelta(days=3)).isoformat(),
        "event_end": make_aware(datetime.now() + timedelta(days=4)).isoformat(),
        "concert_hall": concert_hall.id,
        "artists": [],
    }
    response = api_client.post("/api/events/organizer/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["organizer"] == organizer_user.id

@pytest.mark.django_db
def test_organizer_can_update_own_event(api_client, organizer_user, event_object):
    api_client.force_authenticate(user=organizer_user)
    data = {
        "title": "Concert Modifié",
        "event_start": event_object.event_start.isoformat(),
        "event_end": event_object.event_end.isoformat(),
        "concert_hall": event_object.concert_hall.id,
        "organizer": organizer_user.id,
        "artists": [user.id for user in event_object.artists.all()]
    }
    response = api_client.put(f"/api/events/organizer/{event_object.id}/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Concert Modifié"

@pytest.mark.django_db
def test_organizer_cannot_delete_event(api_client, organizer_user, event_object):
    api_client.force_authenticate(user=organizer_user)
    response = api_client.delete(f"/api/admin/events/{event_object.id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN

# ======= ADMIN ACCESS FULL =======

@pytest.mark.django_db
def test_admin_can_delete_event(api_client, admin_user, event_object):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f"/api/admin/events/{event_object.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_admin_can_create_event(api_client, admin_user, concert_hall, organizer_user):
    api_client.force_authenticate(user=admin_user)
    data = {
        "title": "Super Event",
        "event_start": make_aware(datetime.now() + timedelta(days=10)).isoformat(),
        "event_end": make_aware(datetime.now() + timedelta(days=11)).isoformat(),
        "concert_hall": concert_hall.id,
        "organizer": organizer_user.id,
        "artists": [],
    }
    response = api_client.post("/api/admin/events/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["organizer"] == organizer_user.id
