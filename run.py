#run.py


import pygame  # Import Pygame for graphics and game logic
import sys  # Import sys for system-specific parameters and functions
from agent import Agent  # Import the Agent class from the agent module
from environment import Environment  # Import the Environment class from the environment module


# Constants for screen and grid settings
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  # Dimensions of the main window
GRID_SIZE = 40  # Size of each cell in the grid
STATUS_WIDTH = 300  # Width of the status panel on the side


# Color constants for various elements
BACKGROUND_COLOR = (255, 255, 255)  # White background
BARRIER_COLOR = (0, 0, 0)  # Black barriers
TASK_COLOR = (255, 0, 0)  # Red tasks
TEXT_COLOR = (0, 0, 0)  # Black text
BUTTON_COLOR = (0, 200, 0)  # Green buttons
BUTTON_HOVER_COLOR = (0, 255, 0)  # Brighter green for hover effect
BUTTON_TEXT_COLOR = (255, 255, 255)  # White text for buttons
MOVEMENT_DELAY = 100  # Delay in milliseconds for agent movement 200
AGENT_COLOR = (128, 0, 128)  # blue color


def draw_grid(screen, width, height, grid_size):
    """
    Draw a grid on the screen to help visualize the environment.


    :param screen: Pygame screen to draw on
    :param width: Width of the screen
    :param height: Height of the screen
    :param grid_size: Size of each grid cell
    """
    for x in range(0, width, grid_size):  # Draw vertical grid lines
        for y in range(0, height, grid_size):  # Draw horizontal grid lines
            pygame.draw.rect(screen, (200, 200, 200), (x, y, grid_size, grid_size), 1)


def main():
    """Main function to run the simulation."""
    pygame.init()  # Initialize all Pygame modules
    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))  # Create the main screen
    pygame.display.set_caption("AI Grid Simulation: UCS vs A*")  # Set the window title
    clock = pygame.time.Clock()  # Create a clock to control frame rate
    font = pygame.font.Font(None, 15)  # Set the font for text rendering


    # Initialize the environment and agent
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)  # Create the environment 5
    initial_task_locations = environment.task_locations.copy()  # this method Save initial task locations for resets
    initial_barrier_locations = environment.barrier_locations.copy()  # Save initial barrier locations for resets
    agent = Agent(environment, GRID_SIZE)  # Create the agent
    all_sprites = pygame.sprite.Group()  # Group to manage all sprites for visulaize object
    all_sprites.add(agent)  # Add the agent to the sprite group


    algorithm = "UCS"  # Default algorithm to UCS (Uniform Cost Search)
    simulation_started = False  # Flag to track if the simulation has started
    efficiency_metrics = {"UCS": {"total_cost": 0}, "A*": {"total_cost": 0}}  # Store efficiency metrics for both algorithms


    # Button dimensions and positions
    button_width, button_height = 100, 50  # Dimensions of the buttons
    start_button_x = WINDOW_WIDTH + (STATUS_WIDTH - button_width) // 2  # Center the Start button in the status panel
    start_button_y = WINDOW_HEIGHT // 2 - button_height // 2  # Vertical position for Start button
    start_button_rect = pygame.Rect(start_button_x, start_button_y, button_width, button_height)  # Rect for Start button
    toggle_button_y = start_button_y + button_height + 20  # Vertical position for Toggle button
    toggle_button_rect = pygame.Rect(start_button_x, toggle_button_y, button_width, button_height)  # Rect for Toggle button


    last_move_time = pygame.time.get_ticks()  # Track the time of the last movement


    while True:  # Main game loop
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close event
                pygame.quit()  # Quit Pygame
                sys.exit()  # Exit the program
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse clicks
                if start_button_rect.collidepoint(event.pos):  # If Start button is clicked
                    simulation_started = True  # Start the simulation
                elif toggle_button_rect.collidepoint(event.pos):  # If Toggle button is clicked
                    algorithm = "A*" if algorithm == "UCS" else "UCS"  # Switch between UCS and A*
                    agent.reset_agent()  # Reset the agent's state
                    environment.task_locations = initial_task_locations.copy()  # Reset tasks
                    environment.barrier_locations = initial_barrier_locations.copy()  # Reset barriers
                    simulation_started = False  # Stop the simulation


        # Draw background and grid
        screen.fill(BACKGROUND_COLOR)  # Fill the screen with the background color
        draw_grid(screen, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE)  # Draw the grid


        # Draw tasks
        for (x, y), task_number in environment.task_locations.items():
            pygame.draw.rect(screen, TASK_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Draw task as red square
            text = font.render(str(task_number), True, TEXT_COLOR)  # Render task number as text
            screen.blit(text, (x * GRID_SIZE + GRID_SIZE // 4, y * GRID_SIZE + GRID_SIZE // 4))  # Draw task number


        # Draw barriers
        for x, y in environment.barrier_locations:
            pygame.draw.rect(screen, BARRIER_COLOR, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))  # Draw barriers as black squares


        # Simulate agent movement
        if simulation_started and not agent.is_done():  # If simulation is running and agent has not done it task
            current_time = pygame.time.get_ticks()  # Get current time
            if current_time - last_move_time > MOVEMENT_DELAY:  # If enough time has passed since the last move
                if not agent.moving:  # If the agent is not currently moving
                    agent.plan_tasks(algorithm)  # Plan tasks using the selected algorithm
                    efficiency_metrics[algorithm]["total_cost"] = agent.total_path_cost  # Update efficiency metrics
                else:
                    agent.move()  # Move the agent
                last_move_time = current_time  # Update last move time


        # Update and draw sprites
        all_sprites.update()  # Update all sprites
        all_sprites.draw(screen)  # Draw all sprites


        # Handle button hover effects and draw buttons
        if start_button_rect.collidepoint(pygame.mouse.get_pos()):  # Check if mouse is over Start button
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, start_button_rect)  # Highlight button
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect)  # Draw normal button


        if toggle_button_rect.collidepoint(pygame.mouse.get_pos()):  # Check if mouse is over Toggle button
            pygame.draw.rect(screen, (0, 0, 255), toggle_button_rect)  # Highlight Toggle button in blue
        else:
            pygame.draw.rect(screen, (0, 0, 255), toggle_button_rect)  # Draw normal Toggle button


        # Render and position button texts
        start_text = font.render("Start", True, BUTTON_TEXT_COLOR)  # Render "Start" text
        screen.blit(start_text, (start_button_x + (button_width - start_text.get_width()) // 2,
                                 start_button_y + (button_height - start_text.get_height()) // 2))  # Center "Start" text on button


        toggle_text = font.render(f"Switch to {'A*' if algorithm == 'UCS' else 'UCS'}", True, BUTTON_TEXT_COLOR)  # Render toggle text
        screen.blit(toggle_text, (start_button_x + (button_width - toggle_text.get_width()) // 2,
                                  toggle_button_y + (button_height - toggle_text.get_height()) // 2))  # Center toggle text on button


        # Display status panel
        efficient_algorithm = "UCS" if efficiency_metrics["UCS"]["total_cost"] < efficiency_metrics["A*"]["total_cost"] else "A*"  # Determine more efficient algorithm
        status_text = [
            f"1. Algorithm: {algorithm}",  # Display current algorithm
            f"2. Tasks Completed: {len(agent.completed_tasks)}",  # Number of completed tasks
            "Completed Tasks:",  # Header for completed tasks
        ]


        # Add completed tasks and their costs to the status panel
        completed_tasks_str = ", ".join([f"{task} (Cost: {cost})" for task, cost in agent.completed_tasks])
        status_text.append(completed_tasks_str)
        status_text += [
            f"Path Cost (UCS): {efficiency_metrics['UCS']['total_cost']}",  # Display UCS path cost
            f"Path Cost (A*): {efficiency_metrics['A*']['total_cost']}",  # Display A* path cost
            f"Efficient Algorithm: {efficient_algorithm}"  # Display the more efficient algorithm
        ]


        # Render and display status text line by line
        line_y = 10  # Starting Y position for text
        for line in status_text:
            text = font.render(line, True, TEXT_COLOR)  # Render each line
            screen.blit(text, (WINDOW_WIDTH + 10, line_y))  # Draw line on status panel
            line_y += 30  # Increment Y position for next line


        pygame.display.flip()  # Update the screen
        clock.tick(60)  # Limit the frame rate to 60 FPS


    pygame.quit()  # Quit Pygame
    sys.exit()  # Exit the program


if __name__ == "__main__":
    main()  # Run the main function


