from datetime import datetime
import json
import sys


class Task:
    def __init__(self):
        self.id = None
        self.description = None
        self.status = "todo"
        self.createdAt = str(datetime.now())
        self.updatedAt = self.createdAt


commands = [
    "Add Task", "Update Task", "Delete Task", "Mark Task As In Progress", "Mark Task As Done", "List Tasks",
]

command_input = [
    "add", "update", "delete", "mark-in-progress", "mark-done", "list (Optional Filter: done, todo, in-progress)",
]

task_list = []  # Start with an empty list of objects that will be filled in with data from a JSON file.


def main():
    load_json()
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")  # Needs at least two arguments.
        return
    command = sys.argv[1]
    args = sys.argv[2:]
    # The first input is the command. The other inputs are the necessary arguments for the command.

    if command == "help":
        print_commands()
    elif command == "add":
        add_task(args)
    elif command == "update":
        update_task(args)
    elif command == "delete":
        delete_task(args)
    elif command == "mark-in-progress":
        mark_in_progress(args)
    elif command == "mark-done":
        mark_done(args)
    elif command == "list":
        list_tasks(args)
    else:
        print("Make sure to input a valid command. Type in 'help' if you want to see the valid commands.")


def print_commands():
    print("\n")
    for c_input, command in zip(command_input, commands):
        print(f"{c_input} -> {command}")
    print("\n")


def new_task_id():
    if not task_list:  # If the list is empty, the id of a new task should be 1.
        return 1
    else:
        return max(task.id for task in task_list) + 1


def load_json():
    try:
        with open("task_data.json", "r+") as f:
            f.seek(0)  # Ensures that the file is read from the start.
            try:
                data = json.load(f)
            except json.JSONDecodeError:  # In case the file is empty, the function can stop here.
                return
            for task in data:
                x = Task()
                x.id = (task["id"])
                x.description = (task["description"])
                x.status = (task["status"])
                x.createdAt = (task["createdAt"])
                x.updatedAt = (task["updatedAt"])
                task_list.append(x)
    except FileNotFoundError:
        with open("task_data.json", "w+") as f:
            return
    # Since each task object is stored in the JSON as a dictionary, uses the key-value pairs of each dictionary
    # to rebuild the task objects and store them in task_list.


def save_to_json():
    try:
        with open("task_data.json", "r+") as f:
            f.seek(0)
            f.truncate()  # Clears the current data on the file so that it can be overwritten by the new data.
            json.dump([task.__dict__ for task in task_list], f, indent=4)
    except FileNotFoundError:
        with open("task_data.json", "w+") as f:
            f.seek(0)
            f.truncate()
            json.dump([task.__dict__ for task in task_list], f, indent=4)


def add_task(args):
    if not args:
        print("Error: Please make sure to enter a short description of the task.")
        return
    x = Task()
    x.id = new_task_id()
    x.description = " ".join(args)
    task_list.append(x)
    save_to_json()
    print(f"Task added successfully (ID: {x.id})")


def update_task(args):
    if not args:
        print("Error: Please make sure to enter both the ID of the task you want to update and the new description. "
              "(Make sure to place at least one space between your inputs")
        return
    try:
        x_id = args[0]
        x_description = " ".join(args[1:])
        for task in task_list:
            if task.id == int(x_id):
                task.description = x_description
                task.updatedAt = str(datetime.now())
                save_to_json()
                print(f"Task updated successfully (ID: {task.id})")
                return
        print(f"ID: {x_id} does not exist. Please enter a correct task ID.")
    except ValueError:
        print("Please make sure to enter two values. The first value should be an integer."
              " Also separate both values by at least one space.")


def delete_task(args):
    if not args:
        print("Error: Please make sure to enter the ID of the task you want to delete.")
        return
    try:
        target_id = args[0]
        for task in task_list:
            if task.id == int(target_id):
                task_list.remove(task)
                save_to_json()
                print(f"Task deleted successfully (ID: {task.id})")
                return
        print(f"ID: {target_id} does not exist. Please enter a correct task ID.")
    except ValueError:
        print("Please ensure to enter a valid ID. It must be an integer.")


def mark_in_progress(args):
    if not args:
        print("Error: Please make sure to enter the ID of the task you want mark as in-progress.")
        return
    try:
        x_id = args[0]
        for task in task_list:
            if task.id == int(x_id):
                task.status = "in-progress"
                task.updatedAt = str(datetime.now())
                save_to_json()
                print(f"Task has been marked as in-progress (ID: {task.id})")
                return
        print(f"ID: {x_id} does not exist. Please enter a correct task ID.")
    except ValueError:
        print("Please make sure that you enter a singular integer value.")


def mark_done(args):
    if not args:
        print("Error: Please make sure to enter the ID of the task you want mark as done.")
        return
    try:
        x_id = args[0]
        for task in task_list:
            if task.id == int(x_id):
                task.status = "done"
                task.updatedAt = str(datetime.now())
                save_to_json()
                print(f"Task has been marked as done (ID: {task.id})")
                return
        print(f"ID: {x_id} does not exist. Please enter a correct task ID.")
    except ValueError:
        print("Please make sure that you enter a singular integer value.")


def list_tasks(args):
    if not task_list:
        print("You do not have any saved tasks.")
        return
    if not args:  # No filter provided
        for task in task_list:
            print(f"\nID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created at: {task.createdAt}")
            print(f"Updated at: {task.updatedAt}\n")
        return
    elif args[0] == "done":
        list_done_tasks()
    elif args[0] == "todo":
        list_todo_tasks()
    elif args[0] == "in-progress":
        list_in_progress_tasks()
    else:
        print("Please make sure to enter a valid filter command. (done, todo, in-progress)")
    # Call a specific function if the filter is requested.


def list_done_tasks():
    x = False
    for task in task_list:
        if task.status == "done":
            print(f"\nID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created at: {task.createdAt}")
            print(f"Updated at: {task.updatedAt}\n")
            x = True
    if x is False:
        print("There are no tasks that are marked as 'done'.")


def list_todo_tasks():
    x = False
    for task in task_list:
        if task.status == "todo":
            print(f"\nID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created at: {task.createdAt}")
            print(f"Updated at: {task.updatedAt}\n")
            x = True
    if x is False:
        print("There are no tasks that are marked as 'todo'.")


def list_in_progress_tasks():
    x = False
    for task in task_list:
        if task.status == "in-progress":
            print(f"\nID: {task.id}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status}")
            print(f"Created at: {task.createdAt}")
            print(f"Updated at: {task.updatedAt}\n")
            x = True
    if x is False:
        print("There are no tasks that are marked as 'in-progress'.")


if __name__ == "__main__":  # Ensures code only runs if this is run directly.
    main()
