# Cse366_Ucs_vs_A-
This is my first repository task

This repository contains the implementation of Uniform Cost Search (UCS) and A Search (A)** algorithms for pathfinding in a grid environment. The simulation is built using Python and Pygame and provides a comparative analysis of the two algorithms in navigating through a grid environment with tasks and barriers.


# Table of Contents
    1.Introduction
    2.Setup
    3.Running the Simulation
    4.Grid-Based Pathfinding Simulation Using UCS and A* Algorithms
    5.Code Structure
    6.Features
    7.Challenges Faced and Resolutions

    
 # Introduction 
This lab explores autonomous navigation using an agent-based model in a grid environment. The agent completes tasks while avoiding barriers, implementing Uniform Cost Search (UCS) and A Search (A)** to demonstrate key concepts in optimal pathfinding and heuristic-driven navigation.


# Setup

 1. Requirements
 2.Python 3.13.0 or later
 3.Pygame library

# Installation

Clone this repository to your local machine:

  git clone https://github.com/Riyasaha256/Cse366_Ucs_vs_A-.git

  Navigate to the repository:

  cd .\ucs_vs_a\

  Install Pygame if it's not already installed:

   pip install pygame

# Running the Simulation
The project contains its own run.py file for execution. 

1.Execute the run.py script:
     python run.py

# Grid-Based Pathfinding Simulation Using UCS and A* Algorithms

This project implements an agent-based model for autonomous navigation in a grid environment. The agent navigates the grid to complete tasks while avoiding barriers, using Uniform Cost Search (UCS) and A Search (A)** algorithms. The simulation demonstrates efficient and optimal pathfinding by comparing these two techniques in dynamic scenarios.

 # Features
  
Optimal Pathfinding: Implements UCS and A* algorithms to calculate efficient paths while avoiding barriers.

Enhanced Agent Behavior: Dynamically recalculates and chooses the nearest task for efficient task completion.

Algorithm Efficiency Comparison: Compares the performance and path costs of UCS and A* .


 # Usage
 1. Run run.py in ucs_vs_a directory.
 2. The agent dynamically recalculates paths using UCS or A*, efficiently completing tasks while avoiding barriers. Use the toggle feature to switch between algorithms and observe their behavior.


# Code Structure    

The project contains the following main files:

agent.py: Defines the Agent class, responsible for the agent's properties, movement, and pathfinding using UCS and A*.
environment.py: Defines the Environment class, managing the grid setup, task and barrier placement, and utility functions for path calculations.
main.py: The main script that initializes the Pygame window, environment, and agent, and handles user inputs, algorithm toggling, and display rendering.


# Features

General Features

1. Grid Navigation: The agent moves within a grid to reach designated task locations while avoiding barriers.
2. Pathfinding Algorithms: Implements both Uniform Cost Search (UCS) and A* Search (A*) to demonstrate different pathfinding strategies.
3. Dynamic Visualization: Tasks, barriers, and agent movement are visualized in real-time on the grid.
4. Toggling Functionality: Switch seamlessly between UCS and A* algorithms during the simulation to compare their behavior and efficiency.

# Challenges Faced and Resolutions

1. Grid Initialization
Challenge: Randomly generating tasks and barriers without blocking paths was difficult.
Resolution: Added checks to ensure there is always at least one valid path between the agent and tasks.

2. Algorithm Efficiency
Challenge: A*'s performance relies heavily on the chosen heuristic.
Resolution: Used Manhattan distance, which works efficiently for grid-based navigation.

4. Simulation Display
Challenge: Designing an interface to show algorithm details and path costs was time-consuming.
Resolution: Implemented a side panel to display dynamic information, including the algorithm toggle feature for easy switching between UCS and A*.



     









