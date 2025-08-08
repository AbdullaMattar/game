# Python Level Generator & Solver for Sort Puzzles

## Overview

This repository contains a command-line Python script designed for the procedural generation and analysis of "sort puzzle" games. The tool can create randomized, solvable level configurations and determine the minimum number of moves required for a solution. This is useful for rapidly creating and difficulty-ranking a large set of levels for game development.

## Methodology

The script is composed of two primary components: a level generator and a state-space solver.

### 1\. Level Generation

The `create_level_prototype` function generates a random level layout. The process is as follows:

1.  A balanced pool of items (e.g., colors) is created based on the specified number of colors and tube height.
    
2.  This pool is shuffled to ensure random distribution.
    
3.  The items are sequentially distributed into a predefined number of tubes until the non-empty tubes are full.
    

This method guarantees that every generated level has a valid, sorted end-state, though it does not guarantee solvability from the initial random state.

### 2\. Level Solver

The `solve_level` function analyzes a given level layout to determine its solvability and optimal solution path.

-   **Algorithm**: It employs a **Breadth-First Search (BFS)** algorithm to explore the state space of the puzzle. BFS is ideal for this application as it is guaranteed to find the shortest path (i.e., the minimum number of moves) from the initial state to the solved state.
    
-   **State Representation**: Each unique configuration of the tubes is treated as a node in a graph.
    
-   **Memoization**: A `set` of visited states is maintained to prevent cycles and redundant computations, significantly optimizing the search process. If the queue is exhausted before a solved state is reached, the level is deemed unsolvable.
    

## Usage

The script is executed via the command line and accepts several arguments to configure the generation parameters.

### Prerequisites

-   Python 3.x
    

### Command-Line Interface

**Syntax:**

    python your_script_name.py <colors> <height> <empty_tubes> <output_file> <num_levels> [options]
    

## Output Format

The script generates `.json` files for each valid level found. The file name will be based on the `output_file` argument, appended with an index (e.g., `level_1.json`, `level_2.json`).

The JSON structure includes the minimum move count and the tube configuration:

    {
        "moves": 18,
        "tubes": [
            ["a", "b", "c", "a"],
            ["b", "c", "d", "d"],
            ["a", "b", "c", "d"],
            ["a", "b", "c", "d"],
            [],
            []
        ]
    }

