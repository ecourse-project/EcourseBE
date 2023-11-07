import json
from django.core.management.base import BaseCommand
from apps.system.services.database_services import get_all_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_data = get_all_data()
        json.dump(all_data, open("data_server.json", "w"))
