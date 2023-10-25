from django.core.management.base import BaseCommand

from apps.system.services.database_services import import_database


class Command(BaseCommand):
    def handle(self, *args, **options):
        import_database("data_server.json")
