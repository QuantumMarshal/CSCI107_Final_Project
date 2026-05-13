"""
Project Management System - Backend

This module handles the core data structures and file persistence for the application.
It utilizes a class-based hierarchy to manage projects and tasks, saving data
to a local JSON-based database.

"""

import os
import json

from datetime import datetime

class Data:
    """
    Base class for all data objects in the system.

    Attributes:
        title (str): The primary name or identifier.
        description (str, optional): Additional details about the object.
    """

    def __init__(self, title, description=None):
        self.data = {"title": title, "description": description}

    def get_data(self):
        """Returns the dictionary representation of the object."""
        return self.data

    def __str__(self):
        return json.dumps(self.data)

class TaskData(Data):
    """
    Represents an individual task with a due date and completion status.
    Inherits from Data.
    """
    def __init__(self, title, description=None, due_date=None):
        super().__init__(title, description)
        self.data["due_date"] = due_date
        self.is_done = False

    def check_done(self):
        self.is_done = True

    def check_not_done(self):
        self.is_done = False

class ProjectData(Data):
    """
    Represents a project which contains a collection of tasks.
    Inherits from Data.
    """
    def __init__(self, title, description=None):
        super().__init__(title, description)
        self.data['tasks'] = []

    def add_task(self, task):
        """ Add a new task to the project's task list"""
        self.data['tasks'].append(task)

    def set_tasks(self, tasks):
        """Overrides the entire task list."""
        self.data['tasks'] = tasks

    def get_tasks(self):
        """Returns the list of tasks"""
        return self.data['tasks']

    def get_name(self):
        """Returns the project title."""
        return self.data['title']

    def get_description(self):
        """Returns the project description."""
        return self.data['description']

class Manager:
    """
    The orchestrator for data persistence and retrieval.
    Manages interactions between the UI and the JSON file system.
    """
    def __init__(self, folder_name="database"):
        # Set up path to the local database folder
        self.data_path = os.path.join(os.getcwd(), folder_name)
        self.data = []

        # Create database directory if it doesn't exist
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
            print(f"Created new database folder at: {self.data_path}")

    def get_data(self):
        """Load all JSON files from the data path."""
        self.data = []
        dir_list = os.listdir(self.data_path)

        for file in dir_list:
            with open(os.path.join(self.data_path, file), "r") as f:
                data_dict = json.load(f)
                data = ProjectData(data_dict["title"], data_dict["description"])
                data.set_tasks(data_dict["tasks"])
                self.data.append(data)

    def get_description(self, project_name):
        """Get the description for a specific project by name."""
        for project in self.data:
            if project.get_name() == project_name:
                return project.get_description()

        return None

    def get_all_tasks(self):
        """Get all tasks from all projects into the list"""
        tasks = []
        for project in self.data:
            for task in project.get_tasks():
                tasks.append(task)

        return tasks

    def get_task_from_name(self, project_name):
        """Returns the list of tasks for a given project name."""
        for project in self.data:
            if project.get_name() == project_name:

                return project.get_tasks()

        return None

    def cal_project(self):
        """Returns the total count of projects in the database."""
        return len(self.data)

    def save_file(self, file_name="New Project", description=None, tasks=None):
        """
        Saves or updates a project's JSON file.

        Args:
            file_name (str): Title of the project.
            description (str): Detailed text for the project.
            tasks (list, optional): A new task list item to append.
        """

        file_name = file_name.replace(" ", "_")
        project_data = None

        # Check if project exists in memory, otherwise create it
        for project in self.data:
            if project.get_name() == file_name:
                project_data = project
                break
            else:
                project_data = ProjectData(file_name, description)

        if tasks is not None:
            project_data.add_task(tasks)

        file_path = os.path.join(self.data_path, f"{file_name}.json")

        try:
            with open(file_path, mode="w", encoding="utf-8") as json_file:
                json.dump(project_data.get_data(), json_file, indent=4, sort_keys=True)
            print(f"Successfully created: {file_path}")
        except Exception as e:
            print(f"An error occurred while creating the file: {e}")

    def create_project(self, file_name = "New Project", description=None):
        """Initializes a new project file if the name is not already taken."""
        dir_list = os.listdir(self.data_path)
        print(f"Dir lst: {dir_list}")

        file_name_JSON = file_name + ".json"

        if file_name_JSON in dir_list:
            print(f"Project {file_name} already exists")

        else:
            self.save_file(file_name, description)


    def create_task(self, project_name, title, description, due_date):
        """Appends a new task entry to a specific project file."""
        for project in self.data:
            if project.get_name() == project_name:
                self.save_file(project_name, description, tasks=[title, description, due_date, False])

    def is_valid_date(self, date_string):
        """Validates that a string matches the YYYY-MM-DD format."""
        try:
            # Tries to parse the string into a date object
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def update_task_status(self, project_name, task_title):
        """Toggles the boolean completion status of a specific task and saves the file."""
        file_name = project_name.replace(" ", "_") + ".json"
        file_path = os.path.join(self.data_path, file_name)

        for project in self.data:
            # print(project, project.get_name(), project.get_name()==project_name)
            if project.get_name() == project_name:
                tasks = project.get_tasks()

                # Search for the task by name (index 0 is the title)
                for task in tasks:
                    if task[0] == task_title:
                        task[3] = not task[3]  # Update the boolean (index 3)
                        break

                # Save the updated project data back to the database
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(project.get_data(), f, indent=4, sort_keys=True)
                except Exception as e:
                    print(f"Error saving task status: {e}")
                break

        # Get a new data
        self.get_data()

    def __str__(self):
        return str(self.data_path) + " " +  str(self.data)

if __name__ == "__main__":
    manager = Manager()
    print(manager)

    file_name = input("Enter file name: ")
    manager.create_project(file_name)
    manager.get_data()
    print(manager)
