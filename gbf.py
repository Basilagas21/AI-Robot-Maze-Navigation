class Node:
    def __init__(self, position, parent=None, action=None, h_cost=float('inf')):
        self.position = position
        self.parent = parent
        self.action = action
        self.h_cost = h_cost
        self.entry_order = 0  # Add entry order tracking

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_neighbors(position, grid_rows, grid_cols, obstacles):
    x, y = position
    possible_moves = [
        ("up", (x, y-1)),
        ("down", (x, y+1)),
        ("left", (x-1, y)),
        ("right", (x+1, y))
    ]

    valid_moves = []
    for action, (new_x, new_y) in possible_moves:
        # Check bounds
        if 0 <= new_x < grid_cols and 0 <= new_y < grid_rows:
            # Check obstacles
            is_valid = True
            for obs_x, obs_y, width, height in obstacles:
                if (obs_x <= new_x < obs_x + width and 
                    obs_y <= new_y < obs_y + height):
                    is_valid = False
                    break
            if is_valid:
                valid_moves.append((action, (new_x, new_y)))
    
    return valid_moves

def gbf(start_pos, goals, grid_rows, grid_cols, obstacles):
    # Initialize start node and check if already at goal
    start_node = Node(start_pos)
    if start_pos in goals:
        return [], [], {}
    
    print("\nGreedy Best-First Exploration Path:")
    print(f"Starting at: {start_pos}")
    
    # Set up initial node with heuristic cost
    target_goal = goals[0]
    start_node.h_cost = manhattan_distance(start_pos, target_goal)
    start_node.entry_order = 0
    
    # Initialize search data structures
    frontier = [start_node]         # List of nodes to explore
    explored = set()                # Set of explored positions
    visited_positions = []          # Order of positions visited
    entry_count = 1                 # Counter for tie-breaking
    metrics = {
        'nodes_visited': 0,
        'nodes_explored': 0,
        'path_cost': 0,
        'h_costs': {}              # Store heuristic costs for visualization
    }
    
    while frontier:
        # Sort frontier by h_cost and entry_order for tie-breaking
        frontier.sort(key=lambda x: (x.h_cost, x.entry_order))
        node = frontier.pop(0)      # Get node closest to goal
        current_pos = node.position
        
        if current_pos not in explored:
            # Process current node
            explored.add(current_pos)
            visited_positions.append(current_pos)
            metrics['h_costs'][current_pos] = node.h_cost
            metrics['nodes_visited'] += 1
            
            # Check if goal reached
            if current_pos == target_goal:
                # Reconstruct path from goal to start
                path = []
                current = node
                while current.parent is not None:
                    path.append(current.action)
                    current = current.parent
                
                metrics['path_cost'] = len(path) if path else 0
                metrics['nodes_explored'] = len(explored)
                return path[::-1], visited_positions, metrics
            
            # Explore neighbors
            for action, next_pos in get_neighbors(current_pos, grid_rows, grid_cols, obstacles):
                # Add unexplored neighbors to frontier
                if next_pos not in explored and not any(n.position == next_pos for n in frontier):
                    child = Node(next_pos, node, action)
                    child.h_cost = manhattan_distance(next_pos, target_goal)
                    child.entry_order = entry_count
                    entry_count += 1
                    metrics['h_costs'][next_pos] = child.h_cost
                    frontier.append(child)
    
    return None, visited_positions, metrics
