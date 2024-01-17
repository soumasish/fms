import argparse
from simulator import Simulator
import asyncio
import websockets


async def run_simulator(simulator):
    async with websockets.connect(simulator.uri) as websocket:
        listen_task = asyncio.create_task(simulator.listen_for_messages(websocket))
        console_task = asyncio.create_task(simulator.console_interface(websocket))
        await asyncio.gather(listen_task, console_task)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run websocket client for a specific robot.")
    parser.add_argument("robot_id", type=int, help="ID of the robot")
    parser.add_argument("location_id", type=int, help="ID of the location")
    parser.add_argument("--run", action="store_true", help="Run the simulator")
    args = parser.parse_args()

    if args.run:
        simulator = Simulator(args.robot_id, args.location_id)
        asyncio.run(run_simulator(simulator))
    else:
        print("Please specify --run to start the simulator.")