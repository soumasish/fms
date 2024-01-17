from rest_framework import serializers
from .models import Task, Factory, Location


class FactorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Factory
        fields = ['factory_id', 'factory_name']


class LocationSerializer(serializers.ModelSerializer):
    north = serializers.PrimaryKeyRelatedField(read_only=True)
    northeast = serializers.PrimaryKeyRelatedField(read_only=True)
    southeast = serializers.PrimaryKeyRelatedField(read_only=True)
    south = serializers.PrimaryKeyRelatedField(read_only=True)
    southwest = serializers.PrimaryKeyRelatedField(read_only=True)
    northwest = serializers.PrimaryKeyRelatedField(read_only=True)
    factory = serializers.PrimaryKeyRelatedField(queryset=Factory.objects.all())

    class Meta:
        model = Location
        fields = [
            'location_id',
            'location_name',
            'x_coordinate',
            'y_coordinate',
            'north',
            'northeast',
            'southeast',
            'south',
            'southwest',
            'northwest',
            'factory'
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_id', 'description', 'start_time', 'end_time', 'robot']
