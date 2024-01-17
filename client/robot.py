class Robot:
    def __init__(self, robot_id, location_id):
        self.robot_id = robot_id
        self.location_id = location_id
        self.assigned_tasks = []
        self.completed_tasks = []

    def update_location(self, new_location_id):
        self.location_id = new_location_id

    def assign_task(self, task):
        self.assigned_tasks.append(task)
        print(f"Task {task} assigned to robot {self.robot_id}")

    def complete_task(self, task):
        if task in self.assigned_tasks:
            self.assigned_tasks.remove(task)
            self.completed_tasks.append(task)
            print(f"Task {task} completed by robot {self.robot_id}")
        else:
            print(f"Task {task} not found in assigned tasks for robot {self.robot_id}")
