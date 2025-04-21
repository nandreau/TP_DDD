from django.core.management.base import BaseCommand
from django.core.management import call_command
from datetime import datetime
import os

class Command(BaseCommand):
    help = "Sauvegarde toute la base dans data/backup/YYYY_MM_DD/db_backup.json"

    def handle(self, *args, **kwargs):
        today = datetime.today().strftime('%Y_%m_%d')
        backup_dir = os.path.join('data', 'backup', today)
        os.makedirs(backup_dir, exist_ok=True)

        path = os.path.join(backup_dir, 'db_backup.json')

        with open(path, 'w', encoding='utf-8') as f:
            call_command('dumpdata', '--indent=2', stdout=f)

        self.stdout.write(self.style.SUCCESS(f"✅ Sauvegarde terminée : {path}"))
