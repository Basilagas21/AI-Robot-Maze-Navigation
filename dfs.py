# Node class for representing positions in the search space
class Node:
    def __init__(self, position, parent=None, action=None):
        self.position = position  # Current (x,y) coordinates
        self.parent = parent      # Reference to parent node for path reconstruction
        self.action = action      # Action taken to reach this node

# Helper function to find valid neighboring positions
def get_neighbors(position, grid_rows, grid_cols, obstacles):
    x, y = position
    # Define possible moves in specific order for DFS path
    # Order matters for DFS as it will explore in this sequence
    possible_moves = [
        ("up", (x, y-1)),
        ("down", (x, y+1)),
        ("left", (x-1, y)),
        ("right", (x+1, y))
    ]
    
    valid_moves = []
    for action, (new_x, new_y) in possible_moves:
        # Check if move is within grid boundaries
        if 0 <= new_x < grid_cols and 0 <= new_y < grid_rows:
            # Check if move avoids obstacles
            is_valid = True
            for obs_x, obs_y, width, height in obstacles:
                if (obs_x <= new_x < obs_x + width and 
                    obs_y <= new_y < obs_y + height):
                    is_valid = False
                    break
            if is_valid:
                valid_moves.append((action, (new_x, new_y)))
    
    # Reverse to get LIFO behavior with desired priority
    valid_moves.reverse()
    return valid_moves

# Depth-First Search implementation
def dfs(start_pos, goals, grid_rows, grid_cols, obstacles):
    start_node = Node(start_pos)
    target_goal = goals[0]  # Use first goal as target
    
    frontier = [start_node]           # Stack for DFS frontier
    explored = set()                  # Set to track explored positions
    visited_positions = []            # List to track order of visited positions
    backtrack_stack = []              # Stack to keep track of backtracking positions
    
    while frontier:
        # Get the next node from the frontier (LIFO - last in, first out)
        node = frontier.pop()
        current_pos = node.position
        
        # Process node if not already explored
        if current_pos not in explored:
            explored.add(current_pos)
            visited_positions.append(current_pos)
            backtrack_stack.append(node)  # Add to backtrack stack
            
            # Check if current position is the goal
            if current_pos == target_goal:
                # Reconstruct path from goal to start
                path = []
                current = node
                while current.parent is not None:
                    path.append(current.action)
                    current = current.parent
                return path[::-1], visited_positions, {
                    'nodes_visited': len(visited_positions),
                    'nodes_explored': len(explored),
                    'path_cost': len(path) if path else 0,
                    'search_cost': len(frontier) + len(explored)
                }
            
            neighbors = get_neighbors(current_pos, grid_rows, grid_cols, obstacles)
            
            # If no unvisited neighbors, try backtracking
            if not any(next_pos not in explored for _, next_pos in neighbors):
                # Keep popping from backtrack stack until we find a node with unvisited neighbors
                while backtrack_stack and not any(next_pos not in explored for _, next_pos in get_neighbors(backtrack_stack[-1].position, grid_rows, grid_cols, obstacles)):
                    backtrack_stack.pop()
                
                # If we have a valid backtrack point, add it to frontier
                if backtrack_stack:
                    backtrack_node = backtrack_stack[-1]
                    frontier.append(backtrack_node)
                    continue
            
            # Add unvisited neighbors to frontier
            for action, next_pos in neighbors:
                if next_pos not in explored:
                    child = Node(next_pos, node, action)
                    frontier.append(child)
    
    # Return None if no path found
    return None, visited_positions, {}
