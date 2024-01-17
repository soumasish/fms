import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Factory(Base):
    factory_id = models.AutoField(primary_key=True)
    factory_name = models.CharField(null=True, max_length=256)


class Location(Base):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=256)
    x_coordinate = models.IntegerField()
    y_coordinate = models.IntegerField()
    north = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='south_of')
    northeast = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='southwest_of')
    southeast = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='northwest_of')
    south = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='north_of')
    southwest = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='northeast_of')
    northwest = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='southeast_of')
    factory = models.ForeignKey(Factory, null=True, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"Location {self.location_id}"

    def set_adjacent(self, north=None, northeast=None, southeast=None, south=None, southwest=None, northwest=None):
        self.north = north
        self.northeast = northeast
        self.southeast = southeast
        self.south = south
        self.southwest = southwest
        self.northwest = northwest
        self.save()


class Robot(Base):
    robot_id = models.AutoField(primary_key=True)
    robot_name = models.CharField(null=True, max_length=256)
    current_location = models.OneToOneField(Location, null=True, on_delete=models.SET_NULL)
    factory = models.ForeignKey(Factory, null=True, on_delete=models.CASCADE)
    is_idle = models.BooleanField(default=True)


class Obstacle(Base):

    class ObstacleType(models.TextChoices):
        Table = "TABLE", _("TABLE")
        Chair = "CHAIR", _("CHAIR")

    obstacle_id = models.AutoField(primary_key=True)
    obstacle_type = models.CharField(max_length=256, choices=ObstacleType.choices, default=ObstacleType.Table)
    current_location = models.ManyToManyField(Location)
    factory = models.ForeignKey(Factory, null=True, on_delete=models.CASCADE)


class Task(Base):
    task_id = models.AutoField(primary_key=True)
    description = models.TextField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    robot = models.ForeignKey(Robot, null=True, on_delete=models.SET_NULL)
