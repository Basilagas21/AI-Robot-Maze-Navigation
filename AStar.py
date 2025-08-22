import heapq

class Node:
    def __init__(self, position, parent=None, action=None):
        self.position = position    # Current (x,y) coordinates
        self.parent = parent        # Reference to parent node
        self.action = action        # Action taken to reach this node
        self.entry_order = 0        # For tie-breaking in priority queue

class PriorityQueueItem:
    def __init__(self, f_cost, entry_order, position):
        self.f_cost = f_cost       # Total cost (g_cost + h_cost)
        self.entry_order = entry_order  # For consistent tie-breaking
        self.position = position    # Current position
    
    def __lt__(self, other):
        # Custom comparison for priority queue ordering
        return (self.f_cost, self.entry_order) < (other.f_cost, other.entry_order)

def manhattan_distance(pos1, pos2):
    # Calculate Manhattan distance: |x1-x2| + |y1-y2|
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
        if 0 <= new_x < grid_cols and 0 <= new_y < grid_rows:
            is_valid = True
            for obs_x, obs_y, width, height in obstacles:
                if (obs_x <= new_x < obs_x + width and 
                    obs_y <= new_y < obs_y + height):
                    is_valid = False
                    break
            if is_valid:
                valid_moves.append((action, (new_x, new_y)))
    return valid_moves

def astar(start_pos, goals, grid_rows, grid_cols, obstacles):
    if start_pos in goals:
        return [], [], {}
    
    target_goal = goals[0]
    visited = set()
    priority_queue = []
    entry_count = 0
    
    # Initialize costs dictionary
    all_costs = {}
    all_costs[start_pos] = {
        'g': 0,
        'h': manhattan_distance(start_pos, target_goal),
        'f': manhattan_distance(start_pos, target_goal)
    }
    
    print("\nA* Exploration Path:")
    print(f"Starting at: {start_pos}")
    
    # Initialize start node in priority queue with f_cost = h_cost (g_cost = 0)
    heapq.heappush(priority_queue, PriorityQueueItem(0, entry_count, start_pos))
    
    # Track path and costs
    came_from = {start_pos: (None, None)}  # Maps position to (parent, action)
    cost_so_far = {start_pos: 0}           # g_cost for each position
    visited_positions = []                  # Order of positions visited

    while priority_queue:
        current_item = heapq.heappop(priority_queue)
        current_pos = current_item.position
        
        if current_pos not in visited:
            visited.add(current_pos)
            visited_positions.append(current_pos)
            
            # Check if goal reached
            if current_pos == target_goal:
                # Reconstruct path
                path = []
                current = current_pos
                while current != start_pos:
                    parent, action = came_from[current]
                    path.append(action)
                    current = parent
                
                return path[::-1], visited_positions, {
                    'nodes_visited': len(visited_positions),
                    'nodes_explored': len(visited),
                    'path_cost': len(path) if path else 0,
                    'search_cost': len(priority_queue) + len(visited),
                    'costs': all_costs
                }

            # Explore neighbors
            for action, next_pos in get_neighbors(current_pos, grid_rows, grid_cols, obstacles):
                # Calculate new g_cost for neighbor
                new_g_cost = cost_so_far[current_pos] + 1
                
                # Update costs if better path found
                if next_pos not in cost_so_far or new_g_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_g_cost
                    h_cost = manhattan_distance(next_pos, target_goal)
                    f_cost = new_g_cost + h_cost  # f = g + h
                    
                    # Store costs for visualization
                    all_costs[next_pos] = {
                        'g': new_g_cost,
                        'h': h_cost,
                        'f': f_cost,
                        'display': f"f:{f_cost} g:{new_g_cost} h:{h_cost} "
                    }
                    
                    # Add to priority queue with new f_cost
                    heapq.heappush(priority_queue, PriorityQueueItem(f_cost, entry_count, next_pos))
                    came_from[next_pos] = (current_pos, action)

    return None, visited_positions, {}
