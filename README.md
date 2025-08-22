# Robot Navigation Pathfinding Visualizer 🤖

 
A Python-based interactive visualization tool for comparing various pathfinding algorithms on a grid-based map with obstacles, built using **Pygame**.

## 🧭 Overview

This repository contains the complete codebase for the "Robot Navigation Pathfinding Visualizer." The application allows users to select from a range of common search algorithms to find paths through a grid with defined start, goal, and obstacle positions. It provides real-time visual feedback on the exploration process, displays the resulting path, and dynamically renders a search tree for a deeper understanding of each algorithm's behavior.

## ✨ Features

### 🔍 Algorithm Visualization

* **Multiple Algorithms:** Implements and visualizes six popular pathfinding algorithms:

  * Breadth-First Search (BFS)

  * Depth-First Search (DFS)

  * Greedy Best-First Search (GBF)

  * A\* Search

  * Bidirectional BFS

  * Beam Search

* **Real-time Exploration:** Watch algorithms explore the grid step-by-step.

* **Path Highlighting:** Clearly displays the shortest or found path.

### 🗺️ Interactive Grid

* **Customizable Maps:** Configure grid dimensions, start position, goal(s), and obstacles via the `Map.txt` file.

* **Visual Cues:**

  * **Red Square:** Represents the **start position**.

  * **Green Square(s):** Represent the **goal position(s)**.

  * **Gray Squares:** Represent **obstacles**.

  * **Light Blue Squares:** Represent **visited/explored nodes** by the algorithm.

  * **Yellow Squares:** Represent the **final path** found.

  * **Blue Square:** Represents the **currently exploring node** (during real-time visualization).

### 🌳 Search Tree Visualizer

* **Dynamic Tree Generation:** A search tree is built and displayed alongside the grid, illustrating the nodes expanded and their parent-child relationships.

* **Scroll Functionality:** Navigate large search trees using the mouse wheel.

### 📊 Performance Metrics

* **Key Statistics:** Provides metrics for each algorithm, including:

  * Nodes Visited

  * Nodes Explored

  * Path Cost (number of steps)

## 🛠️ Technologies Used

### Core Stack

| Technology | Purpose | 
 | ----- | ----- | 
| **Python** | Main programming language | 
| **Pygame** | Cross-platform set of Python modules for video game development | 

### Libraries

| Library | Purpose | 
 | ----- | ----- | 
| `heapq` | Heap queue (priority queue) implementation for A\* search | 
| `collections.deque` | Optimized list-like container with fast appends and pops from either end (used in some BFS variants) | 

## 📁 Project Structure

```
.
├── AStar.py                     # A* Search algorithm implementation
├── BeamBFS.py                   # Beam Search algorithm implementation
├── BidirectionalBFS.py          # Bidirectional BFS algorithm implementation
├── Map.txt                      # Configuration file for grid, start, goals, and obstacles
├── Menu.py                      # Main entry point of the application
├── bfs.py                       # Breadth-First Search (BFS) algorithm implementation
├── dfs.py                       # Depth-First Search (DFS) algorithm implementation
├── gbf.py                       # Greedy Best-First Search (GBF) algorithm implementation
├── script.py                    # Main Pygame application logic, UI rendering, and algorithm orchestration
└── searchtree.py                # TreeVisualizer class for rendering search trees
```

## ⚙️ Setup Instructions

### Prerequisites

Before running the program, ensure you have **Python 3.x** installed.

```
python --version
```

### Installation

1. **Ensure all provided Python files are in the same directory:** `AStar.py`, `BeamBFS.py`, `bfs.py`, `BidirectionalBFS.py`, `dfs.py`, `gbf.py`, `Map.txt`, `Menu.py`, `script.py`, and `searchtree.py`.

2. **Install Pygame:** If you don't have it already, install Pygame using pip:

   ```
   pip install pygame
   ```

### Running the Program

To launch the pathfinding visualizer, execute the `Menu.py` file from your terminal:

```
python Menu.py
```

This will open the Pygame application window, displaying the grid visualization.

## 📖 Usage Guide

The application provides an interactive environment to explore pathfinding algorithms.

### 🧭 Interactive Elements

| Element | Description | 
 | ----- | ----- | 
| **Algorithm Buttons** | Located at the bottom of the grid. Click to select and run a specific pathfinding algorithm. | 
| **Grid Display** | The left panel shows the search area, obstacles, start/goal nodes, explored path, and the final path. | 
| **Search Tree** | The right panel visualizes the search process as a tree. Use your **mouse wheel to scroll** if needed. | 
| **Metrics** | Below the grid, key performance indicators for the active algorithm are displayed. | 

### 🚀 Workflow

1. **Launch the application** using `python Menu.py`.

2. **Observe the initial grid**, showing the start position (red), goal(s) (green), and any obstacles (gray) as defined in `Map.txt`.

3. **Select an algorithm** by clicking its corresponding button (e.g., "BFS", "ASTAR").

4. **Watch the visualization** unfold as the algorithm explores the grid and the search tree grows.

5. **Review the final path** (yellow) and the **performance metrics**.

6. **Experiment with different algorithms** to compare their efficiency and pathfinding strategies.

## 🧠 Algorithms Implemented

* **Breadth-First Search (BFS):** An unweighted graph search that explores all nodes at the current depth level before moving to the next. **Guarantees the shortest path** (in terms of number of moves) in unweighted graphs.

* **Depth-First Search (DFS):** Explores as far as possible along each branch before backtracking. **Not guaranteed to find the shortest path** and can be inefficient in large or infinite search spaces.

* **Greedy Best-First Search (GBF):** Expands nodes closest to the goal based on a heuristic function (e.g., Manhattan distance). It's **fast but not optimal**; it may not find the shortest path.

* **A\* Search:** Combines the benefits of Uniform-Cost Search and Greedy Best-First Search. It uses both the cost from the start node (`g`) and a heuristic estimate to the goal (`h`) to determine the next node to explore (`f = g + h`). **Guaranteed to find the optimal path** if the heuristic is admissible and consistent.

* **Bidirectional BFS:** Runs two BFS searches simultaneously, one from the start and one from the goal. When the two frontiers meet, a path is found. Can be **faster than a single BFS** by effectively reducing the search space.

* **Beam Search:** A heuristic search algorithm that explores a graph by expanding the most promising nodes in a limited set. It maintains a "beam" (a fixed number) of the best nodes at each level. It's **not guaranteed to be optimal or complete** but can be useful for reducing computational complexity.

## ⚙️ Configuration File: `Map.txt`

The `Map.txt` file allows you to define the search environment:

The format is as follows:

1. **Grid Dimensions:** `[rows,cols]`

   * Example: `[5,11]` (5 rows, 11 columns)

2. **Start Position:** `(x,y)`

   * Example: `(0,1)`

3. **Goal Positions:** `(x1,y1) | (x2,y2) | ...` (multiple goals separated by `|`)

   * Example: `(7,0) | (10,3)`

4. **Obstacles:** Each line represents an obstacle `(x,y,width,height)`

   * `x,y`: Top-left corner coordinates of the obstacle.

   * `width,height`: Dimensions of the obstacle.

   * Example: `(2,0,2,2)` (An obstacle starting at (2,0) with width 2 and height 2)

## 🤝 Contributing

We welcome contributions! If you have suggestions for improvements or new features, please:

1. Fork the repository.

2. Create a new branch (`git checkout -b feature/your-feature-name`).

3. Make your changes.

4. Commit your changes (`git commit -m 'Add new feature'`).

5. Push to the branch (`git push origin feature/your-feature-name`).

6. Open a Pull Request.

## 📄 License

This project is open-source and distributed under the **MIT License**. See the `LICENSE` file (if provided separately) or the license text within the repository for full details.

## 📞 Support

For any questions, issues, or feedback, please open an issue on the GitHub repository.

**Built with exploration in mind!**