import json
import os  # For checking if the file exists

class Task:
    def __init__(self, task_id, title, completed=False):
        self.id = task_id
        self.title = title
        self.completed = completed

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"ID: {self.id}, Title: {self.title}, Status: {status}"

    def to_dict(self):
        return {"id": self.id, "title": self.title, "completed": self.completed}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["title"], data["completed"])


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.used_ids = set()
        self.counter = 1000
        self.load_tasks()  # Ensure this is calling the method correctly

    def generate_unique_id(self):
        while True:
            self.counter += 1
            task_id = (self.counter * 3) % 10000 + 1234
            if task_id not in self.used_ids:
                self.used_ids.add(task_id)
                return task_id

    def add_task(self, title):
        task_id = self.generate_unique_id()
        task = Task(task_id, title)
        self.tasks.append(task)
        print(f"Task added: {task}")
        self.save_tasks()

    def add_multiple_tasks(self, count):
        for i in range(count):
            title = input(f"Enter title for task {i + 1}: ")
            self.add_task(title)

    def view_tasks(self):
        if not self.tasks:
            print("No tasks available.")
        else:
            header = f"{'ID':<10} | {'Title':<30} | {'Status':<10}"
            print(header)
            print("-" * len(header))
            for task in self.tasks:
                status = "Completed" if task.completed else "Pending"
                print(f"{task.id:<10} | {task.title:<30} | {status:<10}")

    def delete_task(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            self.tasks.remove(task)
            self.used_ids.remove(task_id)
            print(f"Task deleted: {task}")
            self.save_tasks()
        else:
            print(f"No task found with ID: {task_id}")

    def mark_task_complete(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task:
            task.completed = True
            print(f"Task marked as completed: {task}")
            self.save_tasks()
        else:
            print(f"No task found with ID: {task_id}")

    def save_tasks(self):
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "used_ids": list(self.used_ids),
        }
        
        # Save the tasks to the file 
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Tasks saved to file.")

    def load_tasks(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.used_ids = set(data.get("used_ids", []))
                    self.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
                    print("Tasks loaded from file.")
            else:
                print("No previous tasks found, starting fresh.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading tasks. Starting fresh.")


def main():
    task_manager = TaskManager()

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Add Multiple Tasks")
        print("3. View Tasks")
        print("4. Delete Task")
        print("5. Mark Task as Complete")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter task title: ")
            task_manager.add_task(title)
        elif choice == "2":
            try:
                count = int(input("Enter the number of tasks to add: "))
                task_manager.add_multiple_tasks(count)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "3":
            task_manager.view_tasks()
        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to delete: "))
                task_manager.delete_task(task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "5":
            try:
                task_id = int(input("Enter task ID to mark as complete: "))
                task_manager.mark_task_complete(task_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
        elif choice == "6":
            print("Exiting Task Manager. Goodbye!")
            task_manager.save_tasks()  # Save tasks on exit
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
