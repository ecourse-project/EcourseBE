import json

from django.core.management.base import BaseCommand
from django.apps import apps
from django.core import serializers


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_models = apps.get_models()
        all_data = []
        for model in all_models:
            data = model.objects.all()
            serialized_data = serializers.serialize("json", data)
            all_data.extend(json.loads(serialized_data))
        json.dump(all_data, open("data_server.json", "w"))
