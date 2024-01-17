from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from fleet.models import Robot, Factory


class Command(BaseCommand):
    help = 'Creates a specified number of robot objects'

    def add_arguments(self, parser):
        parser.add_argument('num_robots', type=int, help='Number of robots to create')
        parser.add_argument('factory_id', type=str, help='UUID of the factory')

    def handle(self, *args, **options):
        num_robots = options['num_robots']
        factory_id = options['factory_id']

        try:
            factory = Factory.objects.get(pk=factory_id)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Factory with id {factory_id} does not exist.'))
            return

        for i in range(num_robots):
            robot = Robot(robot_name=f"Robot {i + 1}", factory=factory)
            robot.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_robots} robots'))

