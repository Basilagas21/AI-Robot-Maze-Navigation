import pygame
from bfs import bfs          # Breadth-First Search
from dfs import dfs          # Depth-First Search
from gbf import gbf          # Greedy Best-First Search
from AStar import astar      # A* Search
from BidirectionalBFS import bd       # Bidirectional Search
from BeamBFS import bs       # Beam Search
from searchtree import TreeVisualizer  

# Initialize Pygame for visualization
pygame.init()

# Define color constants for visualization
WHITE = (255, 255, 255)     # Background color
BLACK = (0, 0, 0)           # Grid lines
RED = (255, 0, 0)           # Start position
GREEN = (0, 255, 0)         # Goal positions
GRAY = (128, 128, 128)      # Obstacles
DARK_GRAY = (100, 100, 100) # Button hover color
BLUE = (0, 0, 255)          # Current position being explored
YELLOW = (255, 255, 0)      # Path found
LIGHT_BLUE = (173, 216, 230)  # Explored positions

# Grid visualization parameters
CELL_SIZE = 60              # Size of each grid cell in pixels
PADDING = 50                # Padding around the grid

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def read_input_file(filename):

    with open(filename, 'r') as file:
        # Read basic grid information
        grid_dims = file.readline().strip()
        start_pos = file.readline().strip()
        goals = file.readline().strip()
        obstacles_lines = [file.readline().strip() for _ in range(100)]
        
        # Process grid dimensions [rows,cols]
        dimensions = grid_dims.strip('[]').split(',')
        rows = int(dimensions[0])
        cols = int(dimensions[1])
        
        # Process start position (x,y)
        start = start_pos.strip('()').split(',')
        start_pos = (int(start[0]), int(start[1]))
        
        # Process multiple goals separated by |
        goals_list = []
        for goal in goals.split('|'):
            pos = goal.strip('() ').split(',')
            goals_list.append((int(pos[0]), int(pos[1])))
        
        # Process obstacles (x,y,width,height)
        obstacles = []
        for line in obstacles_lines:
            if line:
                coords = line.strip('()').split(',')
                obstacles.append(tuple(map(int, coords)))
                
        return rows, cols, start_pos, goals_list, obstacles

def visualize_exploration_and_path(screen, rows, cols, start_pos, goals, obstacles, visited_positions, path, metrics, algorithm_name):
    explored = set()
    final_pos = None
    current_pos = None
    current_metrics = metrics.copy() if metrics else {}
    current_metrics['h_costs'] = {}  # Initialize empty h_costs
    target_goal = goals[0]
    
    # Different handling based on algorithm type
    if algorithm_name in ["GBF", "ASTAR", "BeamBFS"]:
        for visited_pos in visited_positions:
            explored.add(visited_pos)
            if visited_pos in goals:
                final_pos = visited_pos
            
            # Calculate h_cost for current position
            current_metrics['h_costs'][visited_pos] = manhattan_distance(visited_pos, target_goal)
            
            # Get and calculate heuristics for unvisited neighbors
            x, y = visited_pos
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < cols and 0 <= new_y < rows):
                    next_pos = (new_x, new_y)
                    is_valid = True
                    for obs_x, obs_y, width, height in obstacles:
                        if (obs_x <= new_x < obs_x + width and 
                            obs_y <= new_y < obs_y + height):
                            is_valid = False
                            break
                    if is_valid and next_pos not in explored:
                        current_metrics['h_costs'][next_pos] = manhattan_distance(next_pos, target_goal)
            
            draw_grid(screen, rows, cols, start_pos, goals, obstacles, explored, 
                     visited_pos if visited_pos != start_pos else None,
                     None, final_pos, current_metrics, current_pos, algorithm_name)
            pygame.time.wait(100)
    
    else:
        # Non-heuristic algorithms (BFS, DFS, BidirectionalBFS)
        for visited_pos in visited_positions:
            explored.add(visited_pos)
            if visited_pos in goals:
                final_pos = visited_pos
            
            draw_grid(screen, rows, cols, start_pos, goals, obstacles, explored, 
                     visited_pos if visited_pos != start_pos else None,
                     None, final_pos, None, current_pos, algorithm_name)
            pygame.time.wait(100)
    
    # Show the path for all algorithms
    if path:
        path_positions = []
        current_pos = start_pos
        
        for move in path:
            x, y = current_pos
            if move == "up": y -= 1
            elif move == "down": y += 1
            elif move == "left": x -= 1
            elif move == "right": x += 1
            current_pos = (x, y)
            path_positions.append(current_pos)
            draw_grid(screen, rows, cols, start_pos, goals, obstacles, explored, 
                     None, path_positions, final_pos, current_metrics, current_pos, algorithm_name)
            pygame.time.wait(100)

def draw_grid(screen, rows, cols, start_pos, goals, obstacles, explored, current_explore=None, path_positions=None, final_pos=None, metrics=None, agent_pos=None, algorithm_name=None):
    # Calculate grid area dimensions (using only left half of window)
    grid_width = cols * CELL_SIZE + (2 * PADDING)
    
    # Clear only the left half of the screen
    pygame.draw.rect(screen, WHITE, (0, 0, grid_width, screen.get_height()))
    
    # Draw grid in left half
    for row in range(rows):
        for col in range(cols):
            x = col * CELL_SIZE + PADDING
            y = row * CELL_SIZE + PADDING
            pos = (col, row)
            
            # Draw base cell
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            
            # Check if position is valid (not an obstacle)
            is_valid = True
            for obs_x, obs_y, width, height in obstacles:
                if (obs_x <= col < obs_x + width and 
                    obs_y <= row < obs_y + height):
                    is_valid = False
                    break
            
            # Fill explored positions
            if pos in explored:
                pygame.draw.rect(screen, LIGHT_BLUE,
                               (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
            
            # Draw path if exists
            if path_positions and (col, row) in path_positions:
                pygame.draw.rect(screen, YELLOW,
                               (x + 1, y + 1, 
                                CELL_SIZE - 2, CELL_SIZE - 2))
            
            # Draw current exploring position
            if current_explore and (col, row) == current_explore:
                pygame.draw.rect(screen, BLUE,
                               (x + 1, y + 1, 
                                CELL_SIZE - 2, CELL_SIZE - 2))
            
            # Draw start position
            if (col, row) == start_pos:
                pygame.draw.rect(screen, RED,
                               (x + 1, y + 1, 
                                CELL_SIZE - 2, CELL_SIZE - 2))
            
            # Draw agent position
            if agent_pos and (col, row) == agent_pos:
                pygame.draw.rect(screen, BLUE,
                               (x + 1, y + 1, 
                                CELL_SIZE - 2, CELL_SIZE - 2))
                
            # Draw final position (blue square on goal)
            if final_pos and (col, row) == final_pos:
                pygame.draw.rect(screen, BLUE,
                               (x + 1, y + 1, 
                                CELL_SIZE - 2, CELL_SIZE - 2))
            
            # Fill goals (draw last to ensure it's visible)
            if (col, row) in goals and ((col, row) != final_pos):
                pygame.draw.rect(screen, GREEN,
                               (x + 1, y + 1, 
                                CELL_SIZE - 2, CELL_SIZE - 2))
                
            # Fill obstacles
            for obs_x, obs_y, width, height in obstacles:
                if (obs_x <= col < obs_x + width and 
                    obs_y <= row < obs_y + height):
                    pygame.draw.rect(screen, GRAY,
                                   (x + 1, y + 1, 
                                    CELL_SIZE - 2, CELL_SIZE - 2))
                    
            # Display costs for A* algorithm - draw text last to be on top
            if algorithm_name == "ASTAR" and metrics and 'costs' in metrics:
                if pos in metrics['costs']:
                    costs = metrics['costs'][pos]
                    font = pygame.font.Font(None, 15)
                    text = f"g:{costs['g']}h:{costs['h']} f:{costs['f']}" 
                    text = font.render(text, True, BLACK)
                    text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                    screen.blit(text, text_rect)
            # Draw heuristic values for GBF and BeamBFS on top
            elif algorithm_name in ["GBF", "BeamBFS"] and metrics and 'h_costs' in metrics:
                if is_valid and pos in metrics['h_costs']:
                    h_cost = metrics['h_costs'][pos]
                    font = pygame.font.Font(None, 20)
                    text = font.render(f"{h_cost}", True, BLACK)
                    text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                    screen.blit(text, text_rect)
    
    # Add metrics display if available
    metrics_bottom = rows * CELL_SIZE + PADDING + 20
    if metrics and isinstance(metrics, dict):
        font = pygame.font.Font(None, 36)
        metrics_text = [
            f"Algorithm: {algorithm_name}" if algorithm_name else "Algorithm: None",
            f"Nodes Visited: {metrics.get('nodes_visited', 0)}",
            f"Path Cost: {metrics.get('path_cost', 0)} steps",
        ]
        
        for i, text in enumerate(metrics_text):
            text_surface = font.render(text, True, BLACK)
            screen.blit(text_surface, (PADDING, metrics_bottom + i * 30))

    # Add algorithm buttons below the metrics
    button_y = metrics_bottom + 100  # Position buttons below metrics
    button_width = 80
    button_height = 30
    button_margin = 5
    algorithms = ["BFS", "DFS", "GBF", "ASTAR", "BidirectionalBFS", "BeamBFS"]
    
    font = pygame.font.Font(None, 24)
    buttons = []
    
    for i, algo in enumerate(algorithms):
        button_x = PADDING + (i * (button_width + button_margin))
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        # Check if mouse is hovering over button
        mouse_pos = pygame.mouse.get_pos()
        button_color = DARK_GRAY if button_rect.collidepoint(mouse_pos) else GRAY
        
        # Draw button
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        # Draw button text
        text_surface = font.render(algo, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        
        buttons.append((button_rect, algo))
    
    pygame.display.flip()
    return buttons

def print_metrics(algorithm, metrics):
    print(f"\n{algorithm} Search Metrics:")
    print(f"Nodes Visited: {metrics['nodes_visited']}")
    print(f"Nodes Explored: {metrics['nodes_explored']}")
    print(f"Path Cost: {metrics['path_cost']} steps")
    
    print("-" * 40)

def find_path_through_explored(start, end, explored, rows, cols):
    """Find a path through explored nodes between two positions"""
    from collections import deque
    
    def get_adjacent(pos):
        x, y = pos
        adjacent = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < cols and 0 <= new_y < rows and 
                (new_x, new_y) in explored):
                adjacent.append((new_x, new_y))
        return adjacent
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        pos, path = queue.popleft()
        if pos == end:
            return path
        
        for next_pos in get_adjacent(pos):
            if next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return None

def visualize_search_progress(algorithm, screen, start_pos, goals, visited_positions, frontier, explored, metrics=None):
    try:
        from searchtree import TreeVisualizer
        visualizer = TreeVisualizer()
        
        # Create and render the search tree
        tree = visualizer.create_search_tree(
            algorithm,
            start_pos,
            goals,
            visited_positions,
            frontier,
            explored
        )
        
        # Render the tree to a file
        visualizer.render_tree(f'search_tree_{algorithm.lower()}')
                
    except ImportError:
        print("Graphviz not installed. Please install graphviz to view search trees.")

def main(algorithm=None):
    input_file = "Map.txt"  # Default input file
    
    try:
        rows, cols, start_pos, goals, obstacles = read_input_file(input_file)
        
        window_width = (cols * CELL_SIZE + (2 * PADDING)) * 2  # Double the width to accommodate the tree
        window_height = rows * CELL_SIZE + (2 * PADDING) + 200  # Space for buttons
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Robot Navigation")
        
        current_algorithm = algorithm
        running = True
        tree_visualizer = TreeVisualizer()  # Create single instance here
        current_state = {
            'explored': set(),
            'path': None,
            'metrics': None,
            'visited_positions': None,
            'path_positions': None,
            'tree': None  # Add this to store the tree instance
        }
        
        while running:
            # Only redraw if state has changed
            if current_state.get('needs_update', True):
                screen.fill(WHITE)
                buttons = draw_grid(screen, rows, cols, start_pos, goals, obstacles, 
                                    current_state['explored'], None, current_state['path_positions'], 
                                    None, current_state['metrics'], None, current_algorithm)
                
                # Add tree visualization if we have visited positions
                if current_state['visited_positions']:
                    if not current_state['tree']:  # Only create tree if it doesn't exist
                        current_state['tree'] = tree_visualizer.create_search_tree(
                            current_algorithm,
                            start_pos, 
                            goals, 
                            current_state['visited_positions'], 
                            [], 
                            current_state['explored']
                        )
                    current_state['tree'].render_tree(screen, window_width, window_height)
                
                pygame.display.flip()
                current_state['needs_update'] = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for button clicks
                    mouse_pos = pygame.mouse.get_pos()
                    for button_rect, algo in buttons:
                        if button_rect.collidepoint(mouse_pos):
                            current_algorithm = algo
                            if algo == "BFS":
                                path, visited_positions, metrics = bfs(start_pos, goals, rows, cols, obstacles)
                            elif algo == "DFS":
                                path, visited_positions, metrics = dfs(start_pos, goals, rows, cols, obstacles)
                            elif algo == "GBF":
                                path, visited_positions, metrics = gbf(start_pos, goals, rows, cols, obstacles)
                            elif algo == "ASTAR":
                                path, visited_positions, metrics = astar(start_pos, goals, rows, cols, obstacles)
                            elif algo == "BidirectionalBFS":
                                path, visited_positions, metrics = bd(start_pos, goals, rows, cols, obstacles)
                            elif algo == "BeamBFS":
                                path, visited_positions, metrics = bs(start_pos, goals, rows, cols, obstacles)
                            
                            if path:
                                print(f"Path found for {algo}:", '; '.join(path))
                                print_metrics(algo, metrics)
                                
                                # For algorithms that don't naturally track h_costs, add them
                                if algo in ["GBF", "BeamBFS"] and 'h_costs' not in metrics:
                                    metrics['h_costs'] = {}
                                    target_goal = goals[0]
                                    for pos in visited_positions:
                                        metrics['h_costs'][pos] = abs(pos[0] - target_goal[0]) + abs(pos[1] - target_goal[1])
                                
                                # For A*, ensure we're using the costs from the algorithm
                                if algo == "ASTAR" and 'costs' not in metrics:
                                    metrics['costs'] = {}
                                    target_goal = goals[0]
                                    for pos in visited_positions:
                                        g_cost = manhattan_distance(start_pos, pos)
                                        h_cost = manhattan_distance(pos, target_goal)
                                        f_cost = g_cost + h_cost
                                        metrics['costs'][pos] = {
                                            'g': g_cost,
                                            'h': h_cost,
                                            'f': f_cost
                                        }
                                
                                current_state = {
                                    'explored': set(),
                                    'path': None,
                                    'metrics': metrics,
                                    'visited_positions': visited_positions,
                                    'path_positions': None,
                                    'tree': None  # Reset tree when switching algorithms
                                }
                                visualize_exploration_and_path(screen, rows, cols, start_pos, goals, obstacles, 
                                                            visited_positions, path, metrics, algo)
                                # After visualization, store the final state
                                current_state['explored'] = set(visited_positions)
                                current_state['path'] = path
                                # Calculate and store final path positions
                                path_positions = []
                                current_pos = start_pos
                                if path:
                                    for move in path:
                                        x, y = current_pos
                                        if move == "up": y -= 1
                                        elif move == "down": y += 1
                                        elif move == "left": x -= 1
                                        elif move == "right": x += 1
                                        current_pos = (x, y)
                                        path_positions.append(current_pos)
                                current_state['path_positions'] = path_positions
                            else:
                                print(f"No path found for {algo}!")
                elif event.type == pygame.MOUSEWHEEL:
                    # Handle scroll events for the tree visualizer
                    if current_state['tree']:
                        current_state['tree'].handle_event(event)
                        current_state['needs_update'] = True
            
            pygame.display.flip()
        
        pygame.quit()
        
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
