import os
import json


class Task:
    def __init__(self, title, description, status='Incomplete'):
        self.title = title
        self.description = description
        self.status = status

    def __str__(self):
        return f'Title: {self.title}, Description: {self.description}, Status: {self.status}'

    def mark_complete(self):
        self.status = 'Complete'

    def mark_incomplete(self):
        self.status = 'Incomplete'


class TaskManager:
    def __init__(self, file_name='tasks.json'):
        self.file_name = file_name
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                return [Task(**task) for task in json.load(file)]
        return []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.file_name, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
        else:
            print("Invalid task index")

    def update_task(self, index, title=None, description=None, status=None):
        if 0 <= index < len(self.tasks):
            if title:
                self.tasks[index].title = title
            if description:
                self.tasks[index].description = description
            if status:
                self.tasks[index].status = status
            self.save_tasks()
        else:
            print("Invalid task index")

    def list_tasks(self):
        if self.tasks:
            for i, task in enumerate(self.tasks):
                print(f'{i}. {task}')
        else:
            print("No tasks available.")

    def mark_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()
            self.save_tasks()

    def mark_incomplete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_incomplete()
            self.save_tasks()


def main():
    manager = TaskManager()

    while True:
        print("\nTask Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Remove Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            manager.add_task(title, description)
            print("Task added.")
        elif choice == '2':
            print("Task List:")
            manager.list_tasks()
        elif choice == '3':
            manager.list_tasks()
            index = int(input("Enter the task number to update: "))
            title = input("New title (leave blank to keep the current): ")
            description = input("New description (leave blank to keep the current): ")
            status = input("New status (Complete/Incomplete, leave blank to keep current): ")
            manager.update_task(index, title or None, description or None, status or None)
        elif choice == '4':
            manager.list_tasks()
            index = int(input("Enter the task number to remove: "))
            manager.remove_task(index)
            print("Task removed.")
        elif choice == '5':
            manager.list_tasks()
            index = int(input("Enter the task number to mark as complete: "))
            manager.mark_complete(index)
            print("Task marked as complete.")
        elif choice == '6':
            manager.list_tasks()
            index = int(input("Enter the task number to mark as incomplete: "))
            manager.mark_incomplete(index)
            print("Task marked as incomplete.")
        elif choice == '7':
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
