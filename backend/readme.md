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


```bash
python manage.py import_demographics data/Demographic_stats_per_country.csv
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

## Structure

```bash
  concert_generateur/
  ├── manage.py
  ├── db.sqlite3
  ├── core/                  # App unique contenant tous les domaines (users, artists, events, etc.)
  ├── concert_generateur/    # Configuration Django (settings, urls, wsgi...)
  ├── env/                   # Environnement virtuel (non versionné)

```
