from django.core.management.base import BaseCommand

from apps.system.services.database_services import import_database


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default="data_server.json", help='Specify a custom argument')

    def handle(self, *args, **options):
        path = options['path']
        import_database(path)

