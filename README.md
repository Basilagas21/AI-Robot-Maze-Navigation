# AI-Robot-Maze-Navigation
This project provides a Python-based interactive visualization tool for comparing various pathfinding algorithms on a grid-based map with obstacles. Users can select different search algorithms and observe their exploration process and the resulting optimal path.

Features ✨
Multiple Algorithms: Implements and visualizes Breadth-First Search (BFS), Depth-First Search (DFS), Greedy Best-First Search (GBF), A* Search, Bidirectional BFS, and Beam Search.

Interactive Grid: Displays the grid, start position, goal(s), obstacles, explored nodes, and the final path.

Real-time Visualization: Shows the step-by-step exploration of each algorithm.

Search Tree Visualization: Generates a dynamic search tree on the right side of the screen, providing a clearer view of how each algorithm explores nodes.

Metrics Display: Provides key performance metrics for each algorithm, including nodes visited, nodes explored, and path cost.

Configurable Maps: Reads grid dimensions, start position, goal(s), and obstacles from a Map.txt file, allowing for easy customization of scenarios.
Usage 🎮
Once the Pygame window is open:

Grid Display (Left Panel):

Red Square: Represents the start position.

Green Square(s): Represent the goal position(s).

Gray Squares: Represent obstacles.

Light Blue Squares: Represent visited/explored nodes by the algorithm.

Yellow Squares: Represent the final path found.

Blue Square: Represents the currently exploring node (during real-time visualization).

Algorithm Selection (Bottom Panel):

Click on the buttons at the bottom of the grid to select a pathfinding algorithm: BFS, DFS, GBF, ASTAR, BidirectionalBFS, or BeamBFS.

The visualization for the selected algorithm will begin immediately.

Metrics Display:

Below the algorithm selection buttons, you'll see real-time metrics for the currently running algorithm, including "Nodes Visited" and "Path Cost".

Search Tree (Right Panel):

As an algorithm explores the grid, a search tree will be built and displayed on the right side of the screen. This tree visually represents the nodes expanded by the algorithm and their parent-child relationships.

You can scroll through the search tree using your mouse wheel if it's larger than the display area.

Configuration ⚙️
The grid layout, start position, goals, and obstacles are defined in the Map.txt file. You can edit this file to create custom scenarios:

The format of Map.txt is as follows:

Grid Dimensions: [rows,cols]

Example: [5,11] (5 rows, 11 columns)

Start Position: (x,y)

Example: (0,1)

Goal Positions: (x1,y1) | (x2,y2) | ... (multiple goals separated by |)

Example: (7,0) | (10,3)

Obstacles: Each line represents an obstacle (x,y,width,height)

x,y: Top-left corner of the obstacle.

width,height: Dimensions of the obstacle.

Example: (2,0,2,2) (An obstacle starting at (2,0) with width 2 and height 2)

Algorithms Implemented 🧠
Breadth-First Search (BFS): Explores all neighbor nodes at the current depth level before moving on to nodes at the next depth level. Guarantees the shortest path in terms of the number of moves in an unweighted graph.

Depth-First Search (DFS): Explores as far as possible along each branch before backtracking. Not guaranteed to find the shortest path.

Greedy Best-First Search (GBF): Expands the node that is closest to the goal, as estimated by a heuristic function. Can be fast but not optimal.

A* Search: Combines features of Uniform-Cost Search and Greedy Best-First Search. It finds the shortest path by using a heuristic function to estimate the cost from the current node to the goal. Guaranteed to find the optimal path if the heuristic is admissible and consistent.

Bidirectional BFS: Runs two BFS searches simultaneously, one from the start node and one from the goal node. When the two searches meet, a path is found. Can be faster than a single BFS in some cases.

Beam Search: An optimization of best-first search that reduces memory requirements by limiting the number of nodes at each level of the search tree. It uses a heuristic function to select the most promising nodes to expand. Not guaranteed to find the optimal path.