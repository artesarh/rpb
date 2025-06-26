from django.core.management.base import BaseCommand
import subprocess
import sys
import os


class Command(BaseCommand):
    help = 'Start Celery worker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--loglevel',
            default='info',
            help='Celery log level (default: info)'
        )
        parser.add_argument(
            '--concurrency',
            type=int,
            default=2,
            help='Number of worker processes (default: 2)'
        )

    def handle(self, *args, **options):
        loglevel = options['loglevel']
        concurrency = options['concurrency']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting Celery worker with loglevel={loglevel}, concurrency={concurrency}')
        )
        
        try:
            subprocess.run([
                'celery', '-A', 'project', 'worker',
                '--loglevel', loglevel,
                '--concurrency', str(concurrency)
            ], check=True)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Celery worker stopped'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Celery worker failed: {e}')) 