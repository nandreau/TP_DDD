import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Configuration des chemins
DATA_DIR = Path("data")
FIXTURES_DIR = Path("tools/init")
CSV_CONCERTHALL = DATA_DIR / "ConcertHall.csv"
CSV_EVENTS = DATA_DIR / "EventsData.csv"
CSV_DEMOGRAPHICS = DATA_DIR / "Demographic_stats_per_country.csv"
USERS_FILE = FIXTURES_DIR / "initial_user.json"

def make_backup():
    now = datetime.now().strftime("%Y_%m_%d")
    backup_dir = DATA_DIR / now
    backup_file = backup_dir / "db_backup.json"

    if backup_file.exists():
        print(f"ℹ️  Backup déjà existant pour aujourd’hui : {backup_file}")
        return

    backup_dir.mkdir(parents=True, exist_ok=True)
    print(f"🗃️  Sauvegarde de la base dans : {backup_file}")

    with open(backup_file, "w", encoding="utf-8") as f:
        call_command("dumpdata", "--natural-foreign", "--indent", "2", stdout=f)


def flush_db():
    print("🧨 Flush de la base...")
    call_command("flush", "--noinput")

def apply_migrations():
    print("⚙️  Application des migrations...")
    call_command("migrate", interactive=False)

def import_csvs():
    print("🎵 Import des salles de concert...")
    call_command("import_events_concerts", concert_hall=str(CSV_CONCERTHALL), event=str(CSV_EVENTS))

def import_demographics():
    print("🎵 Import des stats...")
    call_command("import_demographics", str(CSV_DEMOGRAPHICS))

def recreate_groups():
    print("🔁 (Re)création des groupes...")
    groups = ["Admin Group", "Artist Group", "Organizer Group"]
    for name in groups:
        Group.objects.get_or_create(name=name)
        print(f"  ✅ Groupe '{name}'")

def recreate_users():
    print("👤 Création des utilisateurs de test...")
    User = get_user_model()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    for user in users:
        u, created = User.objects.update_or_create(
            username=user["username"],
            defaults={
                "email": user["email"],
                "role": user["role"],
                "is_staff": user.get("is_staff", False),
                "is_superuser": user.get("is_superuser", False)
            }
        )
        u.set_password(user["password"])
        u.save()
        print(f"  ✅ {u.username} ({u.role}) {'[créé]' if created else '[mis à jour]'}")

def reset_env():
    make_backup()
    flush_db()
    apply_migrations()
    import_demographics()
    import_csvs()
    recreate_groups()
    assign_group_permissions()
    recreate_users()
    print("\n✅ Environnement réinitialisé avec succès.")

if __name__ == "__main__":
    # Ajouter le dossier projet au path
    sys.path.append(str(Path(__file__).resolve().parents[1]))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "concert_generateur.settings")

    import django
    django.setup()

    # ↪️ Tous les imports Django doivent être après cette ligne :
    from permissions import assign_group_permissions
    from django.core.management import call_command
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    # Maintenant que Django est prêt, tu peux appeler ton reset
    reset_env()
