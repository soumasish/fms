from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from fleet.models import Task, Robot
from fleet.serializers import TaskSerializer


class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        available_robot = Robot.objects.filter(is_idle=True).first()

        if available_robot:
            task = serializer.save(robot=available_robot)
            available_robot.is_idle = False
            available_robot.save()

            factory_id = available_robot.factory.factory_id if available_robot.factory else None
            self.task_assignment(task, available_robot, str(factory_id))
        else:
            # If no available robot, return an appropriate response
            return Response({'error': 'No available robot to assign to task'}, status=status.HTTP_400_BAD_REQUEST)

    def task_assignment(self, task, assigned_robot, group_name):
        channel_layer = get_channel_layer()
        task_data = {
            'task_id': task.task_id,
            'description': task.description,
            'assigned_robot_id': assigned_robot.robot_id,
        }
        # Send the message
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'task_assignment': task_data,
                'type': 'task_assignment'

            }
        )
