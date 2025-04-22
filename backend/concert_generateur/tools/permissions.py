# tools/permissions.py
from django.contrib.auth.models import Group, Permission

def assign_group_permissions():
    print("🔐 Attribution des permissions aux groupes...")

    group_permissions = {
        "Artist Group": [
            "view_event",
            "view_concerthall",
            "can_view_dashboard",
            "view_country"
        ],
        "Organizer Group": [
            "view_event",
            "add_event"
            "view_concerthall",
            "view_country",
            "view_countrydemographics",
            "can_view_dashboard"
        ],
        "Admin Group": [
            # CustomUser
            "add_customuser", "change_customuser", "delete_customuser", "view_customuser",
            # ConcertHall
            "add_concerthall", "change_concerthall", "delete_concerthall", "view_concerthall",
            # Event
            "add_event", "change_event", "delete_event", "view_event",
            # CountryDemographics
            "add_countrydemographics", "change_countrydemographics",
            "delete_countrydemographics", "view_countrydemographics",
            # Country
            "add_country", "change_country", "delete_country", "view_country",
            # Dashboard / test
            "can_view_dashboard"
        ]
    }

    for group_name, perms in group_permissions.items():
        try:
            group = Group.objects.get(name=group_name)
            for codename in perms:
                try:
                    perm = Permission.objects.get(codename=codename)
                    group.permissions.add(perm)
                except Permission.DoesNotExist:
                    print(f"  ⚠️ Permission introuvable : {codename}")
            print(f"  ✅ Permissions appliquées à '{group_name}'")
        except Group.DoesNotExist:
            print(f"❌ Groupe '{group_name}' non trouvé.")
