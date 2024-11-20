# environment.py
import random  # Import random module for generating random numbers


class Environment:
    def __init__(self, width, height, grid_size, num_tasks, num_barriers):
        """
        Initialize the environment with a grid, tasks, and barriers.


        Args:
            width (int): The width of the environment in pixels.
            height (int): The height of the environment in pixels.
            grid_size (int): The size of each grid cell in pixels.
            num_tasks (int): The number of tasks to place in the environment.
            num_barriers (int): The number of barriers to place in the environment.
        """
        self.width = width  # Store the total width of the environment
        self.height = height  # Store the total height of the environment
        self.grid_size = grid_size  # Store the size of each grid cell
        self.columns = width // grid_size  # Calculate the number of columns in the grid
        self.rows = height // grid_size  # Calculate the number of rows in the grid


        # Generate tasks and barriers
        self.task_locations = self.generate_tasks(num_tasks)  # Create tasks with unique locations
        exclude_set = set(self.task_locations.keys())  # Exclude task locations
        self.barrier_locations = self.generate_random_locations(num_barriers, exclude_set)  # Create barriers


    def generate_tasks(self, num_tasks):
        """
        Generate unique task locations with task numbers.


        Args:
            num_tasks (int): The number of tasks to generate.


        Returns:
            dict: A dictionary with task locations as keys and task numbers as values.
        """
        tasks = {}  # Dictionary to store task locations and their task numbers
        for task_number in range(1, num_tasks + 1):  # Assign task numbers starting from 1
            while True:
                # Randomly select a grid location
                location = (random.randint(0, self.columns - 1), random.randint(0, self.rows - 1))
                if location not in tasks:  # Ensure the location is unique
                    tasks[location] = task_number  # Map the location to the task number
                    break  # Exit the loop after finding a valid location
        return tasks


    def generate_random_locations(self, count, exclude=set()):
        """
        Generate unique random locations on the grid, excluding specified locations.


        Args:
            count (int): The number of random locations to generate.
            exclude (set): A set of locations to avoid when generating new locations.


        Returns:
            set: A set of unique random locations.
        """
        locations = set()  # Create an empty set to store unique locations
        while len(locations) < count:  # Repeat until the desired number of locations is generated
            # Generate a random grid location
            location = (random.randint(0, self.columns - 1), random.randint(0, self.rows - 1))
            if location not in exclude:  # Ensure the location is not in the exclude set
                locations.add(location)  # Add the valid location to the set
        return locations


    def is_within_bounds(self, x, y):
        """
        Check if the given coordinates are within the grid boundaries.


        Args:
            x (int): The x-coordinate (column index) to check.
            y (int): The y-coordinate (row index) to check.


        Returns:
            bool: True if the coordinates are within the grid bounds, False otherwise.
        """
        return 0 <= x < self.columns and 0 <= y < self.rows


    def is_barrier(self, x, y):
        """
        Check if the specified grid location contains a barrier.


        Args:
            x (int): The x-coordinate (column index) to check.
            y (int): The y-coordinate (row index) to check.


        Returns:
            bool: True if the location corresponds to a barrier, False otherwise.
        """
        return (x, y) in self.barrier_locations


    def reset_environment(self, num_tasks, num_barriers):
        """
        Reset the environment by regenerating task and barrier locations.


        Args:
            num_tasks (int): The number of tasks to generate.
            num_barriers (int): The number of barriers to generate.
        """
        self.task_locations = self.generate_tasks(num_tasks)  # Regenerate task locations
        exclude_set = set(self.task_locations.keys())  # Exclude task locations
        self.barrier_locations = self.generate_random_locations(num_barriers, exclude_set)  # Regenerate barriers



