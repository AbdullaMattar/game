import argparse
import random
import json
import string
import collections
import os

def solve_level(tubes, tube_height):
    """
    Checks if a level is solvable using a Breadth-First Search (BFS)
    and returns the minimum number of moves required.
    """
    queue = collections.deque([(tubes, 0)])
    visited = {tuple(map(tuple, sorted(tubes)))}

    while queue:
        current_tubes, move_count = queue.popleft()

        is_solved_state = True
        for tube in current_tubes:
            if tube and (len(tube) != tube_height or len(set(tube)) != 1):
                is_solved_state = False
                break
        if is_solved_state:
            return move_count

        for from_idx, from_tube in enumerate(current_tubes):
            if not from_tube:
                continue
            
            top_ball = from_tube[-1]
            if len(set(from_tube)) == 1 and len(from_tube) == tube_height:
                continue

            for to_idx, to_tube in enumerate(current_tubes):
                if from_idx == to_idx:
                    continue
                
                if len(to_tube) < tube_height and (not to_tube or to_tube[-1] == top_ball):
                    next_tubes_state = [list(t) for t in current_tubes]
                    ball = next_tubes_state[from_idx].pop()
                    next_tubes_state[to_idx].append(ball)
                    
                    serialized_state = tuple(map(tuple, sorted(next_tubes_state)))
                    
                    if serialized_state not in visited:
                        visited.add(serialized_state)
                        queue.append((next_tubes_state, move_count + 1))
    
    return None

def create_level_prototype(num_colors, tube_height, emptyt):
    """
    Creates a random level by distributing balls into a random number of bottles.
    """
    num_bottles = num_colors + emptyt
    all_balls = []
    for i in range(num_colors):
        color = string.ascii_lowercase[i]
        all_balls.extend([color] * tube_height)
    
    random.shuffle(all_balls)
    
    tubes = [[] for _ in range(num_bottles)]
    
    for i in range(num_colors):
        for _ in range(tube_height):
            if all_balls:
                tubes[i].append(all_balls.pop())
    
    return tubes

def save_level_to_json(tubes, moves, filename):
    """Saves the level data, including move count, to a JSON file."""
    level_data = {"moves": moves, "tubes": tubes}
    with open(filename, "w") as f:
        json.dump(level_data, f, indent=4)
    print(f"Successfully saved level to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate solvable levels for the bubble sort game.")
    parser.add_argument("colors", help="Number of colors for the level (e.g., 4)", type=int)
    parser.add_argument("height", help="Height of the tubes (usually 4)", type=int)
    parser.add_argument("empty_tubes", help="How many empty tubes are there", type=int)
    parser.add_argument("output_file", help="Base name of the output JSON file (e.g., level.json)")
    parser.add_argument("num_levels", help="Number of levels to generate", type=int)
    # --- NEW ARGUMENTS ADDED ---
    parser.add_argument("--min_moves", help="Minimum required moves for a valid level.", type=int, default=0)
    parser.add_argument("--max_moves", help="Maximum allowed moves for a valid level.", type=int, default=999)
    args = parser.parse_args()

    if not 2 <= args.colors <= 26:
        raise ValueError("Number of colors must be between 2 and 26.")

    base_name, extension = os.path.splitext(args.output_file)
    generated_levels = 0

    # The loop will now continue until the desired number of valid levels are generated
    while generated_levels < args.num_levels:
        level_num = generated_levels + 1
        current_output_file = f"{base_name}_{level_num}{extension}"
        #print(f"\n--- Searching for Level {level_num}/{args.num_levels} (Range: {args.min_moves}-{args.max_moves} moves) ---")

        attempt_count = 0
        while True:
            attempt_count += 1
            
            level_layout = create_level_prototype(args.colors, args.height, args.empty_tubes)
            moves = solve_level(level_layout, args.height)
            
            if moves is not None:
                # --- NEW MOVE COUNT CHECK ADDED ---
                if args.min_moves <= moves <= args.max_moves:
                    print(f"\n>>> {attempt_count}- SOLVABLE in {moves} moves. Within range. Saving. <<<")
                    save_level_to_json(level_layout, moves, current_output_file)
                    generated_levels += 1 # Increment count of successfully generated levels
                    break # Break inner loop to move to the next level number
