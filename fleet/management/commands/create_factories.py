from django.core.management.base import BaseCommand
from fleet.models import Factory


class Command(BaseCommand):
    help = 'Creates a specified number of factory objects'

    def add_arguments(self, parser):
        parser.add_argument('num_factories', type=int, help='Number of factories to create')

    def handle(self, *args, **options):
        num_factories = options['num_factories']

        for i in range(num_factories):
            factory = Factory(factory_name=f"Factory {i+1}")
            factory.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_factories} factories'))