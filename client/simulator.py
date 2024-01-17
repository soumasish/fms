import asyncio
import threading

import websockets
import json
from robot import Robot


class Simulator:

    def __init__(self, robot_id, location_id):
        self.robot = Robot(robot_id, location_id)
        self.uri = "ws://localhost:9001/fleet/manager/1/"
        print(f"Initializing Simulator for robot_id: {self.robot.robot_id}")

    async def send_initial_joined(self, websocket):
        await self.send_joined(websocket)
        await self.listen_for_messages(websocket)

    async def send_joined(self, websocket):
        await websocket.send(json.dumps(
            {"type": "robot_joined",
             "payload": {"robot_id": str(self.robot.robot_id), "location_id": str(self.robot.location_id)}
             }))
        print(f"> Sent robot joined for robotId {self.robot.robot_id} at location_id: {self.robot.location_id}")

    async def send_location_update(self, websocket, location_id):
        await websocket.send(json.dumps(
            {"type": "location_update",
             "payload": {"robot_id": str(self.robot.robot_id), "location_id": str(location_id)}
             }))
        print(f"> Sent location update for robotId {self.robot.robot_id} to location {str(location_id)}")

    async def send_obstacle_update(self, websocket, location_ids):
        if not isinstance(location_ids, list):
            location_ids = [location_ids]
        message = json.dumps({
            "type": "location_update",
            "payload": {
                "robot_id": str(self.robot.robot_id),
                "location_ids": [str(location_id) for location_id in location_ids]
            }
        })
        await websocket.send(message)

        location_ids_str = ', '.join(str(id) for id in location_ids)
        print(f"> Sent location update for robotId {self.robot.robot_id} to locations {location_ids_str}")

    async def send_task_completion_update(self, websocket, task_id):
        await websocket.send(json.dumps(
            {"type": "task_completed",
             "payload": {"robot_id": str(self.robot.robot_id), "task_id": task_id}
             }))
        print(f"> Sent task completion update for robotId {self.robot.robot_id}")

    async def listen_for_messages(self, websocket):
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            if 'robot_joined' in data:
                print(f"< Received robot joined update: {data['robot_joined']}")
            elif 'location_update' in data:
                print(f"< Received location update: {data['location_update']}")
            elif 'task_assignment' in data:
                print(f"< Received task assignment: {data['task_assignment']}")
            elif 'task_completed' in data:
                print(f"< Received task completion: {data['task_completed']}")
            else:
                print(f"< {response}")

    async def console_interface(self, websocket):
        while True:
            command = input("Enter command: ")
            if command.startswith("robot_joined"):
                _, *args = command.split()
                print(args[0])
                location_id = args[0] if args else None
                await self.send_location_update(websocket, location_id)
            elif command.startswith("location_update"):
                _, *args = command.split()
                location_id = args[1] if args else None
                await self.send_location_update(websocket, location_id)
            elif command.startswith("task_completed"):
                _, *args = command.split()
                task_id = args[0] if args else None
                await self.send_location_update(websocket, task_id)
            elif command == "obstacle":
                await self.send_obstacle_update(websocket)
            elif command == "exit":
                break

    def start_console_interface(self, websocket):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.console_interface(websocket))

    async def run(self):
        try:
            async with websockets.connect(self.uri) as websocket:
                # Start console interface in a separate thread
                console_thread = threading.Thread(target=self.start_console_interface, args=(websocket,))
                console_thread.start()

                # Continue with listening for messages
                await self.listen_for_messages(websocket)

                # Join the console thread after listening is done
                console_thread.join()
        except Exception as e:
            print(f"An error occurred: {e}")


