import pygame

class TreeVisualizer:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.node_radius = 20
        self.level_height = 80
        self.node_spacing = 60
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 15
        
        # Colors for different node states
        self.colors = {
            'default': (128, 128, 128),  # Gray for unvisited nodes
            'visited': (173, 216, 230),  # Light blue for visited nodes
            'path': (255, 255, 0),       # Yellow for path nodes
            'start': (255, 0, 0),        # Red for start node
            'goal': (0, 255, 0),         # Green for goal node
            'current': (0, 0, 255)       # Blue for current node
        }

    def create_search_tree(self, algorithm, start_pos, goals, visited_positions, frontier, explored):
        self.nodes = []
        self.edges = []
        
        # Initialize tracking structures
        level_nodes = {0: [start_pos]}
        node_levels = {start_pos: 0}
        parent_map = {}
        
        # Add start node
        self.nodes.append({
            'pos': start_pos,
            'color': self.colors['start'],
            'level': 0,
            'index': 0,
            'visited': True,
            'in_path': False
        })
        
        # Build tree structure from visited positions
        for i in range(1, len(visited_positions)):
            current_pos = visited_positions[i]
            if current_pos in node_levels:
                continue
            
            # Find parent node
            parent_found = False
            for j in range(i-1, -1, -1):
                prev_pos = visited_positions[j]
                if manhattan_distance(prev_pos, current_pos) == 1:
                    parent_map[current_pos] = prev_pos
                    node_levels[current_pos] = node_levels[prev_pos] + 1
                    if node_levels[current_pos] not in level_nodes:
                        level_nodes[node_levels[current_pos]] = []
                    level_nodes[node_levels[current_pos]].append(current_pos)
                    parent_found = True
                    break
            
            if not parent_found:
                node_levels[current_pos] = 1
                if 1 not in level_nodes:
                    level_nodes[1] = []
                level_nodes[1].append(current_pos)
                parent_map[current_pos] = start_pos
            
            # Add node to tree
            node_color = self.colors['visited']
            if current_pos in goals:
                node_color = self.colors['goal']
            
            self.nodes.append({
                'pos': current_pos,
                'color': node_color,
                'level': node_levels[current_pos],
                'index': len(level_nodes[node_levels[current_pos]]) - 1,
                'visited': True,
                'in_path': False
            })
            
            if current_pos in parent_map:
                self.edges.append((parent_map[current_pos], current_pos))
        
        # Get path positions from grid
        path_positions = set()
        current_pos = None
        
        # Find goal position
        for pos in reversed(visited_positions):
            if pos in goals:
                current_pos = pos
                break
        
        # Trace back path from goal to start
        while current_pos and current_pos in parent_map:
            path_positions.add(current_pos)
            current_pos = parent_map[current_pos]
        path_positions.add(start_pos)
        
        # Update node colors for path
        for node in self.nodes:
            if node['pos'] in path_positions:
                node['color'] = self.colors['path']
                node['in_path'] = True
        
        return self

    def render_tree(self, screen, window_width, window_height):
        # Calculate total height needed
        max_level = max(node['level'] for node in self.nodes) if self.nodes else 0
        tree_surface_height = max(window_height, (max_level + 1) * self.level_height + 200)
        
        # Create surface for tree
        tree_surface = pygame.Surface((window_width//2, tree_surface_height))
        tree_surface.fill((255, 255, 255))
        
        # Update maximum scroll limit
        self.max_scroll = max(0, tree_surface_height - window_height)
        
        # Draw edges first
        node_positions = self._calculate_node_positions(window_width)
        self._draw_edges(tree_surface, node_positions)
        
        # Draw nodes
        self._draw_nodes(tree_surface, node_positions)
        
        # Draw scrollbar if needed
        if tree_surface_height > window_height:
            self._draw_scrollbar(screen, window_height)
        
        # Draw the visible portion of the tree surface
        screen.blit(tree_surface, (window_width//2, 0))

    def _calculate_node_positions(self, window_width):
        node_positions = {}
        max_nodes_at_level = {}
        
        # Count nodes at each level
        for node in self.nodes:
            level = node['level']
            if level not in max_nodes_at_level:
                max_nodes_at_level[level] = 0
            max_nodes_at_level[level] += 1
        
        # Calculate positions
        level_counters = {}
        for node in self.nodes:
            level = node['level']
            if level not in level_counters:
                level_counters[level] = 0
            
            total_width = max_nodes_at_level[level] * self.node_spacing
            start_x = (window_width//4) - (total_width//2)
            x = start_x + level_counters[level] * self.node_spacing
            y = 50 + level * self.level_height
            
            node_positions[node['pos']] = (x, y)
            level_counters[level] += 1
        
        return node_positions

    def _draw_edges(self, surface, node_positions):
        for start_pos, end_pos in self.edges:
            if start_pos in node_positions and end_pos in node_positions:
                start_x, start_y = node_positions[start_pos]
                end_x, end_y = node_positions[end_pos]
                
                # Apply scroll offset
                start_y -= self.scroll_y
                end_y -= self.scroll_y
                
                # Draw edge if visible
                if min(start_y, end_y) <= surface.get_height() and max(start_y, end_y) >= 0:
                    # Use yellow for path edges, black for others
                    edge_color = (255, 255, 0) if any(n['pos'] == end_pos and n['in_path'] for n in self.nodes) else (0, 0, 0)
                    pygame.draw.line(surface, edge_color, (start_x, start_y), (end_x, end_y), 2)

    def _draw_nodes(self, surface, node_positions):
        for node in self.nodes:
            x, y = node_positions[node['pos']]
            y -= self.scroll_y
            
            # Only draw if node is within visible area
            if -self.node_radius <= y <= surface.get_height() + self.node_radius:
                pygame.draw.circle(surface, node['color'], (x, y), self.node_radius)
                
                # Draw position text
                font = pygame.font.Font(None, 20)
                text = font.render(str(node['pos']), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x, y))
                surface.blit(text, text_rect)

    def _draw_scrollbar(self, screen, window_height):
        scrollbar_height = (window_height / (self.max_scroll + window_height)) * window_height
        scrollbar_pos = (self.scroll_y / self.max_scroll) * (window_height - scrollbar_height)
        
        # Draw scrollbar background
        pygame.draw.rect(screen, (200, 200, 200), 
                       (screen.get_width() - 20, 0, 20, window_height))
        
        # Draw scrollbar handle
        pygame.draw.rect(screen, (100, 100, 100),
                       (screen.get_width() - 18, scrollbar_pos, 16, scrollbar_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y = max(0, min(self.max_scroll, 
                                   self.scroll_y - event.y * self.scroll_speed))

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
