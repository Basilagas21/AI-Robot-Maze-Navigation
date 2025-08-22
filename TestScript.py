import pygame
import sys
from script import read_input_file, visualize_exploration_and_path
from bfs import bfs


def run_test_case(test_file, output_file=None):
    try:
        # Initialize pygame and create window
        pygame.init()
        
        # Read the test case file
        print(f"\nProcessing test case: {test_file}")
        rows, cols, start_pos, goals, obstacles = read_input_file(test_file)
        print(f"Grid dimensions: {rows}x{cols}")
        print(f"Start position: {start_pos}")
        print(f"Goal position(s): {goals}")
        print(f"Number of obstacles: {len(obstacles)}\n")   
        
        # Create window
        window_width = (cols * 60 + (2 * 50)) * 2
        window_height = rows * 60 + (2 * 50) + 200
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(f"BFS Test - {test_file}")
        
        # Run BFS
        path, visited_positions, metrics = bfs(start_pos, goals, rows, cols, obstacles)
        
        if path:
            print(f"\nTest Case: {test_file}")
            print("Path found:", '; '.join(path))
            print(f"Path length: {len(path)}")
            print(f"Nodes visited: {metrics['nodes_visited']}")
            print("-" * 50)
            
            # Save metrics to output file if specified
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(f"Path: {'; '.join(path)}\n")
                    f.write(f"Path length: {len(path)}\n")
                    f.write(f"Nodes visited: {metrics['nodes_visited']}\n")
                    f.write(f"Nodes explored: {metrics['nodes_explored']}\n")
                    f.write(f"Search cost: {metrics['search_cost']}")
            
            # Visualize the path
            visualize_exploration_and_path(
                screen, rows, cols, start_pos, goals, obstacles,
                visited_positions, path, metrics, "BFS"
            )
            
            # Keep window open until user closes it
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            waiting = False
            
            return True
        else:
            print(f"\nNo path found for {test_file}")
            return False
            
    except FileNotFoundError:
        print(f"Error: {test_file} not found")
        return False
    except Exception as e:
        
        print(f"Error processing {test_file}: {e}")
        return False
    finally:
        pygame.quit()

def run_gui_mode():
    pygame.init()
    
    # List of test cases
    test_cases = [
        "TestCase1.txt",
        "TestCase2.txt",
        "TestCase3.txt",
        "TestCase4.txt",
        "TestCase5.txt",
        "TestCase6.txt",
        "TestCase7.txt",
        "TestCase8.txt",
        "TestCase9.txt",
        "TestCase10.txt"
    ]
    
    for test_file in test_cases:
        run_test_case(test_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single test case mode
        test_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        run_test_case(test_file, output_file)
    else:
        # All test cases mode
        run_gui_mode()
