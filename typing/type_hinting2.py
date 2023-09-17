from typing import List
from datetime import datetime

class Task:
    def __init__(self, title: str, description: str, due_date: datetime):
        self.title = title
        self.description = description
        self.due_date = due_date

def display_task_list(tasks: List[Task]) -> None:
    print("Task List:")
    for i, task in enumerate(tasks, start=1):
        print(f"Task {i}:")
        print(f"Title: {task.title}")
        print(f"Description: {task.description}")
        print(f"Due Date: {task.due_date}")
        print()

# Creating a list of tasks with type hints
tasks = [
    Task("Buy groceries", "Buy milk, eggs, and bread.", "2023-09-20"),
    Task("Write report", "Prepare quarterly report for the team.", "2023-09-25"),
    Task("Exercise", "Go for a 30-minute jog.", "2023-09-21")
]

# Calling the function with type hint
display_task_list(tasks)
