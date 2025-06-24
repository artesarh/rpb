from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "Runs the database backup script"

    def handle(self, *args, **options):
        try:
            subprocess.run(
                ["pg_dump", "-U", "username", "database_name", ">", "backup.sql"],
                check=True,
            )
            self.stdout.write(
                self.style.SUCCESS("Database backup completed successfully.")
            )
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Backup failed: {e}"))
