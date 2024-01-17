from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from fleet.models import Robot, Factory


class Command(BaseCommand):
    help = 'Creates a specified number of robot objects'

    def add_arguments(self, parser):
        parser.add_argument('factory_id', type=str, help='ID of the factory')

    def handle(self, *args, **options):
        factory_id = options['factory_id']

        try:
            factory = Factory.objects.get(pk=factory_id)
        except ObjectDoesNotExist:
            self.stdout.write(self.style.ERROR(f'Factory with id {factory_id} does not exist.'))
            return
        robots = Robot.objects.filter(factory=factory)
        for robot in robots:
            robot.is_idle = True
            robot.current_location = None
            robot.save()

        self.stdout.write(self.style.SUCCESS(f'Reset all robots to idle'))

