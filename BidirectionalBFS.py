class Node:
    def __init__(self, position, parent=None, action=None):
        self.position = position
        self.parent = parent
        self.action = action

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

def get_reverse_action(action):
    if action == "up": return "down"
    if action == "down": return "up"
    if action == "left": return "right"
    if action == "right": return "left"

def reconstruct_path(meet_node_forward, meet_node_backward):
    # Reconstruct forward path
    forward_path = []
    current = meet_node_forward
    while current.parent is not None:
        forward_path.append(current.action)
        current = current.parent
    forward_path = [x for x in forward_path if x is not None]
    forward_path.reverse()  # Reverse to get correct order
    
    # Reconstruct backward path
    backward_path = []
    current = meet_node_backward
    while current.parent is not None:
        if current.action is not None:
            backward_path.append(get_reverse_action(current.action))
        current = current.parent
    
    # Return combined path, filtering out any None values
    return [x for x in (forward_path + backward_path) if x is not None]

# Bidirectional Search implementation
def bd(start_pos, goals, grid_rows, grid_cols, obstacles):
    # Initialize start and goal nodes 
    start_node = Node(start_pos)
    goal_node = Node(goals[0])  # Using first goal
    
    # Early exit if start is goal
    if start_pos in goals:
        return [], [], {}
    
    # Initialize forward and backward search frontiers
    forward_frontier = [start_node]
    backward_frontier = [goal_node]
    forward_explored = {start_pos: start_node}
    backward_explored = {goals[0]: goal_node}
    visited_positions = [start_pos]  # Initialize with start position
     
    while forward_frontier and backward_frontier:
        # Forward search
        if forward_frontier:
            current_forward = forward_frontier.pop(0)
            if current_forward.position not in visited_positions:
                visited_positions.append(current_forward.position)
            
            # Check if forward search meets backward search
            if current_forward.position in backward_explored:
                path = reconstruct_path(current_forward, 
                                     backward_explored[current_forward.position])
                return path, visited_positions, {
                    'nodes_visited': len(visited_positions),
                    'nodes_explored': len(forward_explored) + len(backward_explored),
                    'path_cost': len(path),
                    'search_cost': len(forward_frontier) + len(backward_frontier) + 
                                 len(forward_explored) + len(backward_explored)
                }
            
            # Expand forward search
            for action, next_pos in get_neighbors(current_forward.position, 
                                                grid_rows, grid_cols, obstacles):
                if next_pos not in forward_explored:
                    child = Node(next_pos, current_forward, action)
                    forward_explored[next_pos] = child
                    forward_frontier.append(child)
        
        # Backward search
        if backward_frontier:
            current_backward = backward_frontier.pop(0)
            if current_backward.position not in visited_positions:
                visited_positions.append(current_backward.position)
            
            if current_backward.position in forward_explored:
                path = reconstruct_path(
                    forward_explored[current_backward.position], 
                    current_backward
                )
                return path, visited_positions, {
                    'nodes_visited': len(visited_positions),
                    'nodes_explored': len(forward_explored) + len(backward_explored),
                    'path_cost': len(path),
                    'search_cost': len(forward_frontier) + len(backward_frontier) + 
                                 len(forward_explored) + len(backward_explored)
                }
            
            # Expand backward search
            for action, next_pos in get_neighbors(current_backward.position, 
                                                grid_rows, grid_cols, obstacles):
                if next_pos not in backward_explored:
                    child = Node(next_pos, current_backward, action)
                    backward_explored[next_pos] = child
                    backward_frontier.append(child)
    
    # No path found
    return None, visited_positions, {}
