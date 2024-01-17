import json
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from fleet.models import Robot, Location, Task, Obstacle

logger = logging.getLogger('fleet')


class FleetManagementConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory_id = None
        logger.debug("FleetManagementConsumer initialized")

    def connect(self):
        self.factory_id = str(self.scope['url_route']['kwargs']['factory_id'])
        async_to_sync(self.channel_layer.group_add)(self.factory_id, self.channel_name)
        self.accept()
        logger.info(f"WebSocket connected to Factory ID: {self.factory_id}")

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.factory_id, self.channel_name)
        logger.info(f"WebSocket disconnected from Factory ID: {self.factory_id}")

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message_type = data.get("type")
        if message_type == 'location_update':
            self.handle_location_update(data['payload'])
        elif message_type == 'robot_joined':
            self.handle_robot_joined(data['payload'])
        elif message_type == 'task_completed':
            self.handle_task_completed(data['payload'])

    def handle_robot_joined(self, data):
        robot_id = data['robot_id']
        location_id = data['location_id']
        logger.info(f"Robot joined: Robot ID: {robot_id}, Location ID: {location_id}")
        try:
            robot = Robot.objects.get(pk=int(robot_id))
            location = Location.objects.get(pk=int(location_id))
            robot.current_location = location
            robot.save()
            # broadcast
            async_to_sync(self.channel_layer.group_send)(self.factory_id, {
                'robot_joined': {'robot_id': robot_id, 'location_id': location_id},
                'type': 'robot_joined'})
            # Send a direct response back to the client
            self.send(text_data=json.dumps({'status': '[DM] Receive robot joined update'}))
        except Exception as e:
            self.send(text_data=json.dumps({'status': 'error', 'message': str(e)}))
            logger.error(f"Error processing update: {e}")

    def handle_location_update(self, data):
        robot_id = data['robot_id']
        location_id = data['location_id']
        logger.debug(f"Received location update: Robot ID: {robot_id}, Location: {location_id}")
        try:
            robot = Robot.objects.get(pk=int(robot_id))
            location = Location.objects.get(pk=int(location_id))
            robot.current_location = location
            robot.save()
            # broadcast
            async_to_sync(self.channel_layer.group_send)(self.factory_id, {
                'location_update': {'robot': robot.robot_id, 'location': robot.current_location.location_id},
                'type': 'location_update'})

            # Send a direct response back to the client
            self.send(text_data=json.dumps({'status': '[DM] Received location update'}))
        except Exception as e:
            self.send(text_data=json.dumps({'status': 'error', 'message': str(e)}))
            logger.error(f"Error processing update: {e}")

    def handle_task_completed(self, data):
        robot_id = data['robot_id']
        task_id = data['task_id']
        end_time = data['end_time']
        logger.info(f"Task Completed: Robot ID: {robot_id}, Task ID: {task_id}, End Time: {end_time}")
        try:
            robot = Robot.objects.get(pk=int(robot_id))
            task = Task.objects.get(pk=int(task_id))
            if task.robot == robot:
                task.end_time = end_time
                task.save()
                robot.is_idle = True
                robot.save()
            # broadcast
            async_to_sync(self.channel_layer.group_send)(self.factory_id, {
                'task_completed': {'robot_id': robot_id, 'task_id': task_id, 'end_time': end_time},
                'type': 'task_completed'})
            # Send a direct response back to the client
            self.send(text_data=json.dumps({'status': '[DM] Receive task completion update'}))
        except Exception as e:
            self.send(text_data=json.dumps({'status': 'error', 'message': str(e)}))
            logger.error(f"Error processing update: {e}")

    def handle_obstacle_update(self, data):
        robot_id = data['robot_id']
        location_ids = data['location_ids']
        obstacle_type = data.get('obstacle_type', 'DEFAULT_TYPE')  # Default type if not provided
        logger.debug(
            f"Received location update: Robot ID: {robot_id}, Locations: {location_ids}, Obstacle Type: {obstacle_type}")
        try:
            robot = Robot.objects.get(pk=int(robot_id))
            for location_id in location_ids:
                location = Location.objects.get(pk=int(location_id))

                # Check if an obstacle of the specified type exists in this location
                obstacle_exists = Obstacle.objects.filter(current_location=location,
                                                          obstacle_type=obstacle_type,
                                                          factory_id=robot.factory.factory_id).exists()

                if not obstacle_exists:
                    # Create new obstacle if it doesn't exist
                    new_obstacle = Obstacle(current_location=location, obstacle_type=obstacle_type,
                                            factory_id=robot.factory.factory_id)
                    new_obstacle.save()
                    # Broadcast new obstacle creation
                    async_to_sync(self.channel_layer.group_send)(
                        {'type': 'new_obstacle',
                         'new_obstacle': {'obstacle_id': new_obstacle.obstacle_id, 'obstacle_type': obstacle_type}}
                    )
                    self.send(text_data=json.dumps({'status': '[DM] Received location update'}))
        except Exception as e:
            self.send(text_data=json.dumps({'status': 'error', 'message': str(e)}))
            logger.error(f"Error processing update: {e}")

    def robot_joined(self, event):
        task_data = event['robot_joined']
        self.send(text_data=json.dumps({'robot_joined': task_data}))
        logger.debug(f"Broadcast robot joined: {task_data}")

    def location_update(self, event):
        task_data = event['location_update']
        self.send(text_data=json.dumps({'location_update': task_data}))
        logger.debug(f"Broadcast location update: {task_data}")

    def task_assignment(self, event):
        task_data = event['task_assignment']
        self.send(text_data=json.dumps({'task_assignment': task_data}))
        logger.debug(f"Broadcast task assignment: {task_data}")

    def task_completed(self, event):
        task_data = event['task_completed']
        self.send(text_data=json.dumps({'task_completed': task_data}))
        logger.debug(f"Broadcast task completed: {task_data}")

    def new_obstacle(self, event):
        task_data = event['new_obstacle']
        self.send(text_data=json.dumps({'new_obstacle': task_data}))
        logger.debug(f"Broadcast new obstacle: {task_data}")
