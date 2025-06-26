from django.core.management.base import BaseCommand
import subprocess
import sys


class Command(BaseCommand):
    help = 'Start Celery Beat scheduler'

    def add_arguments(self, parser):
        parser.add_argument(
            '--loglevel',
            default='info',
            help='Celery Beat log level (default: info)'
        )

    def handle(self, *args, **options):
        loglevel = options['loglevel']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting Celery Beat scheduler with loglevel={loglevel}')
        )
        
        try:
            subprocess.run([
                'celery', '-A', 'project', 'beat',
                '--loglevel', loglevel,
                '--scheduler', 'django_celery_beat.schedulers:DatabaseScheduler'
            ], check=True)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Celery Beat stopped'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Celery Beat failed: {e}')) 