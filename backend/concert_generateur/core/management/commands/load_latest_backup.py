from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import glob

class Command(BaseCommand):
    help = "Charge la dernière sauvegarde JSON (ou une date précise) depuis data/backup/"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Affiche la dernière sauvegarde trouvée sans la charger"
        )
        parser.add_argument(
            '--date',
            type=str,
            help="Date de la sauvegarde à charger (format : YYYY_MM_DD)"
        )

    def handle(self, *args, **options):
        base_dir = os.path.join('data', 'backup')

        if not os.path.exists(base_dir):
            self.stdout.write(self.style.ERROR("❌ Aucun dossier 'data/backup' trouvé."))
            return

        # Si une date est fournie
        if options['date']:
            date_folder = options['date']
            backup_path = os.path.join(base_dir, date_folder, 'db_backup.json')
            if not os.path.exists(backup_path):
                self.stdout.write(self.style.ERROR(f"❌ Aucun fichier trouvé pour la date {date_folder}"))
                return
            if options['dry_run']:
                self.stdout.write(f"📁 Fichier de sauvegarde ciblé : {backup_path}")
            else:
                self.stdout.write(f"🔄 Chargement de la sauvegarde : {backup_path}")
                call_command('loaddata', backup_path)
                self.stdout.write(self.style.SUCCESS("✅ Sauvegarde chargée avec succès !"))
            return

        # Sinon on cherche la plus récente
        dated_dirs = sorted(
            [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))],
            reverse=True
        )

        for folder in dated_dirs:
            backup_path = os.path.join(base_dir, folder, 'db_backup.json')
            if os.path.exists(backup_path):
                if options['dry_run']:
                    self.stdout.write(f"📁 Dernière sauvegarde trouvée : {backup_path}")
                else:
                    self.stdout.write(f"🔄 Chargement de la sauvegarde : {backup_path}")
                    call_command('loaddata', backup_path)
                    self.stdout.write(self.style.SUCCESS("✅ Sauvegarde chargée avec succès !"))
                return

        self.stdout.write(self.style.ERROR("❌ Aucune sauvegarde JSON trouvée."))
