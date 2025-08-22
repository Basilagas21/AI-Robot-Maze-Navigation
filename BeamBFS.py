# Node class for tracking positions and their heuristic costs
class Node:
    def __init__(self, position, parent=None, action=None):
        self.position = position  # Current position (x,y)
        self.parent = parent      # Parent node for path reconstruction
        self.action = action      # Action taken to reach this node
        self.h_cost = 0          # Heuristic cost (Manhattan distance to goal)

# Calculate Manhattan distance between two points
def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

# Get valid neighboring positions
def get_neighbors(position, grid_rows, grid_cols, obstacles):
    x, y = position
    possible_moves = [
        ("up", (x, y-1)),
        ("down", (x, y+1)),
        ("left", (x-1, y)),
        ("right", (x+1, y))
    ]
    
    valid_moves = []
    # Check each possible move for validity
    for action, (new_x, new_y) in possible_moves:
        if 0 <= new_x < grid_cols and 0 <= new_y < grid_rows:
            is_valid = True
            # Check for collision with obstacles
            for obs_x, obs_y, width, height in obstacles:
                if (obs_x <= new_x < obs_x + width and 
                    obs_y <= new_y < obs_y + height):
                    is_valid = False
                    break
            if is_valid:
                valid_moves.append((action, (new_x, new_y)))
    
    return valid_moves

# Beam Search implementation
def bs(start_pos, goals, grid_rows, grid_cols, obstacles, beam_width=3):
    if start_pos in goals:
        return [], [], {}
    
    # Initialize start node with heuristic cost
    start_node = Node(start_pos)
    target_goal = goals[0]  # Using first goal
    start_node.h_cost = manhattan_distance(start_pos, target_goal)
    
    frontier = [start_node]
    explored = set()
    visited_positions = []
    
    while frontier:
        # Get all neighbors of current frontier nodes
        next_nodes = []
        for node in frontier:
            if node.position not in explored:
                explored.add(node.position)
                visited_positions.append(node.position)
                
                # Check if goal reached
                if node.position == target_goal:
                    # Reconstruct path
                    path = []
                    current = node
                    while current.parent is not None:
                        path.append(current.action)
                        current = current.parent
                    
                    # Print all visited coordinates in one line
                    print("\nBeam Search Exploration Coordinates:", end=" ")
                    print(", ".join(str(pos) for pos in visited_positions))
                    
                    return path[::-1], visited_positions, {
                        'nodes_visited': len(visited_positions),
                        'nodes_explored': len(explored),
                        'path_cost': len(path),
                        'search_cost': len(frontier) + len(explored)
                    }
                
                # Explore neighbors
                for action, next_pos in get_neighbors(node.position, grid_rows, grid_cols, obstacles):
                    if next_pos not in explored:
                        child = Node(next_pos, node, action)
                        child.h_cost = manhattan_distance(next_pos, target_goal)
                        next_nodes.append(child)
        
        # Select best nodes based on beam width
        next_nodes.sort(key=lambda x: x.h_cost)
        frontier = next_nodes[:beam_width]  # Keep only the best k nodes
        
        if not frontier:  # No more nodes to explore within beam width
            break
    
    # No path found
    return [], visited_positions, {
        'nodes_visited': len(visited_positions),
        'nodes_explored': len(explored),
        'path_cost': 0,
        'search_cost': len(frontier)
    }
