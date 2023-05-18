from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Test command")
        # self.stdout.write('[#] Begin execute...')

