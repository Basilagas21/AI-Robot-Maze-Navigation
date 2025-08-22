# Node class to represent positions in the grid with parent and action tracking
class Node:
    def __init__(self, position, parent=None, action=None):
        self.position = position  # Current position (x,y)
        self.parent = parent      # Parent node for path reconstruction
        self.action = action      # Action taken to reach this node

# Helper function to get valid neighboring positions
def get_neighbors(position, grid_rows, grid_cols, obstacles):
    x, y = position
    # Define possible moves in all four directions
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
            # Check if move collides with obstacles
            is_valid = True
            for obs_x, obs_y, width, height in obstacles:
                if (obs_x <= new_x < obs_x + width and 
                    obs_y <= new_y < obs_y + height):
                    is_valid = False
                    break
            if is_valid:
                valid_moves.append((action, (new_x, new_y)))
    
    return valid_moves

# Breadth-First Search implementation
def bfs(start_pos, goals, grid_rows, grid_cols, obstacles):
    if start_pos in goals:
        return [], [], {}
    
    # Initialize data structures
    queue = [(start_pos, [])]  # (position, path)
    visited = set([start_pos])
    visited_positions = [start_pos]
    
    while queue:
        current_pos, path = queue.pop(0)
        
        # Check if current position is a goal
        if current_pos in goals:
            return path, visited_positions, {
                'nodes_visited': len(visited_positions),
                'nodes_explored': len(visited),
                'path_cost': len(path),
                'search_cost': len(queue) + len(visited)
            }
        
        # Get valid neighbors
        x, y = current_pos
        for dx, dy, action in [(0, -1, "up"), (0, 1, "down"), (-1, 0, "left"), (1, 0, "right")]:
            next_x, next_y = x + dx, y + dy
            next_pos = (next_x, next_y)
            
            # Check if position is valid
            if (0 <= next_x < grid_cols and 0 <= next_y < grid_rows):
                # Check if position is blocked by obstacle
                is_valid = True
                for obs_x, obs_y, width, height in obstacles:
                    if (obs_x <= next_x < obs_x + width and 
                        obs_y <= next_y < obs_y + height):
                        is_valid = False
                        break
                
                if is_valid and next_pos not in visited:
                    visited.add(next_pos)
                    visited_positions.append(next_pos)
                    queue.append((next_pos, path + [action]))
    
    # No path found
    return None, visited_positions, {
        'nodes_visited': len(visited_positions),
        'nodes_explored': len(visited),
        'path_cost': 0,
        'search_cost': len(queue) + len(visited)
    }
