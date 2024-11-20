# agent.py
#agent.py
import pygame
import heapq  # For priority queue in UCS and A* algorithms




class Agent(pygame.sprite.Sprite):
    def __init__(self, environment, grid_size):
        """Initialize the agent."""
        super().__init__()  # Initialize the parent class (pygame.sprite.Sprite)
       
        # Set up the agent's visual representation (a blue square)
        self.image = pygame.Surface((grid_size, grid_size))  # Create a surface for the agent with a size of grid_size
        self.image.fill((0, 0, 255))  # Fill the surface with blue color (RGB: 0, 0, 255)
        self.rect = self.image.get_rect()  # Get the rectangle area of the surface (used for positioning)
       
        # Assign environment and grid properties
        self.grid_size = grid_size  # Grid size (defines the size of each square cell in the grid)
        self.environment = environment  # Store the environment to access tasks, barriers, etc.


        # Agent state
        self.position = [0, 0]  # Initial position of the agent (top-left corner of the grid)
        self.rect.topleft = (0, 0)  # Set the top-left corner of the agent’s rectangle to (0, 0)
        self.task_completed = 0  # Count of tasks the agent has completed
        self.completed_tasks = []  # List to store completed tasks along with their costs
        self.path = []  # List to store the planned path (a sequence of grid coordinates)
        self.moving = False  # Flag to check if the agent is currently moving
        self.total_path_cost = 0  # Total cost of all tasks completed by the agent (used for performance tracking)


    def reset_agent(self):
        """Reset the agent's state to its initial values."""
        self.position = [0, 0]  # Reset position to the start (top-left corner)
        self.rect.topleft = (0, 0)  # Update the agent's visual position to match its grid position
        self.task_completed = 0  # Reset the task count
        self.completed_tasks = []  # Clear the list of completed tasks
        self.path = []  # Clear the current path
        self.moving = False  # Stop the agent’s movement
        self.total_path_cost = 0  # Reset the total path cost


    def move(self):
        """Move the agent one step along its planned path."""
        if self.path:  # Check if there is a planned path
            next_position = self.path.pop(0)  # Get the next position in the path
            self.position = list(next_position)  # Update the agent's position
            self.rect.topleft = (self.position[0] * self.grid_size, self.position[1] * self.grid_size)  # Update visual position
            self.check_task_completion()  # Check if the agent reached a task location
        else:
            self.moving = False  # Stop moving if the path is empty


    def check_task_completion(self):
        """Check if the agent has reached a task location and mark it as completed."""
        position_tuple = tuple(self.position)  # Convert position to a tuple for comparison
        if position_tuple in self.environment.task_locations:  # Check if the agent is on a task location
            task_number = self.environment.task_locations.pop(position_tuple)  # Remove the task from the environment
            self.task_completed += 1  # Increment the task completion counter
            self.completed_tasks.append((task_number, self.total_path_cost))  # Record the task number and total cost


    def plan_tasks(self, algorithm):
        """Plan a path to the nearest task using the selected algorithm."""
        start = tuple(self.position)  # Current position of the agent (as a tuple)
        nearest_task = self.find_nearest_task()  # Find the nearest task to the agent


        if nearest_task:  # If there is a task to plan for
            tasks = [nearest_task]  # List of tasks to target (only one task in this case)
            barriers = self.environment.barrier_locations  # Get the list of barriers (obstacles on the grid)


            # Select the path planning algorithm based on the input
            if algorithm == "UCS":  # If Uniform Cost Search is selected
                self.path, cost = self.uniform_cost_search(start, tasks, barriers)  # Plan the path with UCS
            elif algorithm == "A*":  # If A* Search is selected
                self.path, cost = self.a_star_search(start, tasks, barriers)  # Plan the path with A*


            # Update the agent's total path cost and set the agent to start moving
            self.total_path_cost += cost  # Add the path cost to the total cost
            self.moving = True  # Enable movement


    def find_nearest_task(self):
        """Find the nearest task location based on Manhattan distance."""
        if not self.environment.task_locations:  # If no tasks remain
            return None
        # Find the task that is closest to the current position using Manhattan distance
        return min(self.environment.task_locations.keys(), key=lambda t: abs(t[0] - self.position[0]) + abs(t[1] - self.position[1]))


    def is_done(self):
        """Check if the agent has completed all tasks."""
        return len(self.environment.task_locations) == 0  # Return True if no tasks remain


    def uniform_cost_search(self, start, tasks, barriers):
        """Uniform Cost Search (UCS) to find the shortest path to a task."""
        queue = [(0, start, [])]  # Priority queue with (cost, current_position, path)
        visited = set()  # Set to keep track of visited nodes


        while queue:  # Continue until the queue is empty
            cost, current, path = heapq.heappop(queue)  # Get the node with the lowest cost
            if current in visited:  # Skip if the node has already been visited
                continue
            visited.add(current)  # Mark the node as visited


            path = path + [current]  # Extend the current path with the current node


            if current in tasks:  # If a task is found
                return path[1:], cost  # Return the path (excluding the start position) and cost


            # Explore the neighbors of the current node
            for neighbor in self.get_neighbors(current, barriers):  # Get valid neighbors
                if neighbor not in visited:  # Only add unvisited neighbors to the queue
                    heapq.heappush(queue, (cost + 1, neighbor, path))  # Add the neighbor to the priority queue with updated cost


        return [], 0  # Return empty path and zero cost if no path is found


    def a_star_search(self, start, tasks, barriers):
        """A* Search to find the shortest path to a task."""
        def heuristic(a, b):
            """Heuristic function: Manhattan distance between two points."""
            return abs(a[0] - b[0]) + abs(a[1] - b[1])


        queue = [(0, start, [])]  # Priority queue with (f_cost, current_position, path)
        visited = set()  # Set to keep track of visited nodes
        g_costs = {start: 0}  # Dictionary to store the g_cost (cost from start to each node)


        while queue:  # Continue until the queue is empty
            _, current, path = heapq.heappop(queue)  # Get the node with the lowest f_cost
            if current in visited:  # Skip if the node has already been visited
                continue
            visited.add(current)  # Mark the node as visited


            path = path + [current]  # Extend the current path with the current node


            if current in tasks:  # If a task is found
                return path[1:], g_costs[current]  # Return the path (excluding the start position) and g_cost


            # Explore the neighbors of the current node
            for neighbor in self.get_neighbors(current, barriers):  # Get valid neighbors
                tentative_g_cost = g_costs[current] + 1  # Calculate tentative g_cost for the neighbor
                if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:  # If a better g_cost is found
                    g_costs[neighbor] = tentative_g_cost  # Update g_cost
                    f_cost = tentative_g_cost + min(heuristic(neighbor, task) for task in tasks)  # Calculate f_cost
                    heapq.heappush(queue, (f_cost, neighbor, path))  # Add the neighbor to the priority queue


        return [], 0  # Return empty path and zero cost if no path is found


    def get_neighbors(self, position, barriers):
        """Get valid neighboring positions."""
        x, y = position  # Unpack the current position into x and y
        neighbors = []  # List to store valid neighbors
        directions = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]  # Directions to check


        for _, (dx, dy) in directions:  # Iterate over each direction
            nx, ny = x + dx, y + dy  # Calculate new position
            if self.environment.is_within_bounds(nx, ny) and (nx, ny) not in barriers:  # Check if it's within bounds and not a barrier
                neighbors.append((nx, ny))  # Add valid neighbor to the list


        return neighbors  # Return the list of valid neighbors




