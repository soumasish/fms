from django.core.management.base import BaseCommand
from fleet.models import Location, Factory
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = 'Initializes the factory grid for a specific factory'

    def add_arguments(self, parser):
        parser.add_argument('grid_width', type=int, help='Width of the grid')
        parser.add_argument('grid_height', type=int, help='Height of the grid')
        parser.add_argument('factory_id', type=str, help='UUID of the factory')

    def handle(self, *args, **options):
        grid_width = options['grid_width']
        grid_height = options['grid_height']
        factory_id = options['factory_id']

        try:
            factory = Factory.objects.get(pk=factory_id)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Factory with id {factory_id} does not exist.'))
            return

        def generate_location_name(n):
            name = ""
            while n > 0:
                n, remainder = divmod(n - 1, 26)
                name = chr(65 + remainder) + name
            return name

        # Create locations
        location_counter = 1
        locations = []
        for y in range(grid_height):
            row = []
            for x in range(grid_width):
                location_name = generate_location_name(location_counter)
                location = Location(factory=factory, x_coordinate=x, y_coordinate=y, location_name=location_name)
                location.save()
                row.append(location)
                location_counter += 1
            locations.append(row)

        for row in locations:
            for location in row:
                location.save()

        # Set adjacencies
        for y in range(grid_height):
            for x in range(grid_width):
                location = locations[y][x]
                adjacencies = {
                    'north': locations[y - 1][x] if y > 0 else None,
                    'south': locations[y + 1][x] if y < grid_height - 1 else None,
                    'northeast': locations[y - 1][x + 1] if y > 0 and x < grid_width - 1 else None,
                    'southeast': locations[y + 1][x + 1] if y < grid_height - 1 and x < grid_width - 1 else None,
                    'southwest': locations[y + 1][x - 1] if y < grid_height - 1 and x > 0 else None,
                    'northwest': locations[y - 1][x - 1] if y > 0 and x > 0 else None,
                }
                location.set_adjacent(**adjacencies)

        self.stdout.write(self.style.SUCCESS(f'Successfully initialized grid for Factory {factory_id}'))
