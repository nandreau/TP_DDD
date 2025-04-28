# 🎵 Concert Générateur - Backend Django

Ce projet correspond à l’API backend du générateur de concerts, basé sur Django et Django REST Framework, organisé selon une approche Domain-Driven Design (DDD).

---

## ⚙️ Stack utilisée

- Python 3.10+
- Django 4.x
- Django REST Framework

- Architecture DDD dans une seule app (core/)

## 🚀 Lancer le projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/votre-utilisateur/TD_DDD.git
cd TD_DDD/backend/concert_generateur
```

### 2. Créer un environnement virtuel

```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/Scripts/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

#### Version rapide (load backup)

```bash
python manage.py load_latest_backup
python manage.py makemigrations core
python manage.py migrate
```

#### Version lente (load data)

```bash
python manage.py import_demographics data/Demographic_stats_per_country.csv
python manage.py import_events_concerts --concert_hall="data/ConcertHall.csv" --event="data/EventsData.csv"
python manage.py import_music_data
python manage.py makemigrations core
python manage.py migrate
```

### 5. Créer un superutilisateur (accès à l’admin)


```bash
python manage.py createsuperuser

```

### 6. Lancer le serveur de développement
```bash
python manage.py runserver

```

- Le projet sera disponible à : http://127.0.0.1:8000
- Interface admin : http://127.0.0.1:8000/admin/
- API navigable : endpoints sous /api/

## Générer un événement

Dans Postman, créer une requête POST sur l'endpoint : http://127.0.0.1:8000/api/generate-event/

avec un body JSON :

```json
{
  "country_code": "FR",
  "concert_hall_id": 369,
  "genre_family_name": "Electro",
  "event_start": "2025-05-18T20:00:00",
  "taille_casting": 2,
  "quality_score": 5,
  "custom_title": "SWAG FESTOCHE"
}
```

Puis pour le valider, créer une requête POST sur l'endpoint : http://127.0.0.1:8000/api/validate-event/

avec un body JSON :

```json
{
  "title": "le SWAG FESTOCHE",
  "event_start": "2025-05-18T20:00:00",
  "event_end": "2025-05-18T21:54:00",
  "concert_hall_id": 369,
  "country": "FR",
  "artist_ids": [3834, 4236]
}
```

En sortie :

```json
{
    "message": "Event proposal validated successfully"
}
```

## Structure

```bash
  concert_generateur/
  ├── manage.py
  ├── db.sqlite3
  ├── core/                  # App unique contenant tous les domaines (users, artists, events, etc.)
  ├── data/                  # Données brutes
  ├── concert_generateur/    # Configuration Django (settings, urls, wsgi...)
  ├── env/                   # Environnement virtuel (non versionné)
  ├── requirements.txt       # Dépendances
  ├── readme.md              # Documentation
  ├── tools/                 # Outils pour la gestion du projet

```

Dans core,

```bash
core/
  ├── models/                # Modèles Django
  ├── serializers/           # Sérialiseurs Django REST Framework
  ├── views/                 # Vues Django REST Framework
  ├── urls.py                # URLs Django
  ├── admin.py               # Admin Django
  ├── tests.py               # Tests Django
```

Dans models,

```bash
models/
  ├── artists.py             # Modèle Artist
  ├── concerthalls.py        # Modèle ConcertHall
  ├── countries.py           # Modèle Country
  ├── demographics.py        # Modèle Demographics
  ├── events.py              # Modèle Event
  ├── genres.py              # Modèle Genre
  ├── genres.py              # Modèle Genre
  ├── tracks.py              # Modèle Track
  ├── users.py               # Modèle User
```

Dans serializers,

```bash
serializers/
  ├── artists.py             # Sérialiseur Artist
  ├── concerthalls.py        # Sérialiseur ConcertHall
  ├── countries.py           # Sérialiseur Country
  ├── demographics.py        # Sérialiseur Demographics
  ├── events.py              # Sérialiseur Event
  ├── genres.py              # Sérialiseur Genre
  ├── groups.py              # Sérialiseur Group
  ├── tracks.py              # Sérialiseur Track
  ├── users.py               # Sérialiseur User
```

Dans views,

```bash
views/
  ├── artists.py             # Vue Artist
  ├── concerthalls.py        # Vue ConcertHall
  ├── countries.py           # Vue Country
  ├── demographics.py        # Vue Demographics
  ├── events.py              # Vue Event
  ├── genres.py              # Vue Genre
  ├── groups.py              # Vue Group
  ├── tokens.py              # Vue Token
  ├── tracks.py              # Vue Track
  ├── users.py               # Vue User
```

## Effectuer des tests

```bash
cd backend/concert_generateur
python -m pytest
```

## Documentation

```bash
cd backend/concert_generateur
python manage.py runserver
```

- Swagger : http://127.0.0.1:8000/api/swagger/
- Redoc : http://127.0.0.1:8000/api/redoc/
