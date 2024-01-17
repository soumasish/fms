import asyncio
import random
import websockets
import json
import argparse


class Simulator:
    LOCATIONS = [16, 26, 36, 46, 56, 66, 76, 86]
    OBSTACLE_LOCATIONS = [(4, 5, 6, 7), (11, 12, 13, 14), (21, 22, 23, 24)]

    def __init__(self, robot_id, location_id):
        self.robot_id = robot_id
        self.location_id = location_id
        self.uri = "ws://localhost:9001/fleet/manager/1/"
        print(f"Initializing Simulator for robot_id: {self.robot_id}")

    async def send_joined(self, websocket):
        await websocket.send(json.dumps(
            {"type": "robot_joined",
             "payload": {"robot_id": str(self.robot_id), "location_id": str(self.location_id)}
             }))
        print(f"> Sent robot joined for robotId {self.robot_id} at location_id: {self.location_id}")

    async def send_location_update(self, websocket):
        location_id = random.choice(self.LOCATIONS)
        await websocket.send(json.dumps(
            {"type": "location_update",
             "payload": {"robot_id": str(self.robot_id), "location_id": location_id}
             }))
        print(f"> Sent location update for robotId {self.robot_id}")

    async def send_obstacle_update(self, websocket):
        locations = random.choice(self.OBSTACLE_LOCATIONS)
        await websocket.send(json.dumps(
            {"type": "obstacle_update",
             "payload": {"robot_id": str(self.robot_id), "locations": locations}
             }))
        print(f"> Sent obstacle update from robotId {self.robot_id}")

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
            else:
                print(f"< {response}")

    async def run(self):
        async with websockets.connect(self.uri) as websocket:
            _ = asyncio.create_task(self.listen_for_messages(websocket))
            await self.send_joined(websocket)
            while True:
                await self.send_location_update(websocket)
                await asyncio.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run websocket client for a specific robot.")
    parser.add_argument("robot_id", type=int, help="ID of the robot")
    parser.add_argument("location_id", type=int, help="ID of the location")
    args = parser.parse_args()

    client = Simulator(args.robot_id, args.location_id)
    asyncio.run(client.run())
