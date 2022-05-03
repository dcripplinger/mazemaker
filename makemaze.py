#!/bin/python3

"""
Requires python3 to be installed

Run with ./makemaze.py

This tool creates a 3d maze and provides instructions
to build it in Dragon Quest Builders. The maze is enclosed
in a structure that fits within the space allowed by a sharing
stone in Terra Incognita. The structure looks block-like and
has dimensions of 22 blocks wide, 22 blocks long, and 13 blocks
tall. It floats 1 block above the surface and has an entrance
at the bottom floor at the front and an exit at the top (roof).

The maze is designed by dividing up the structure into 2x2x2
chambers, where each floor is a grid of 7 chambers by 7
chambers, and there are 4 floors. The algorithm starts out by
assuming walls and ceilings between every chamber. It then
executes several random walks to remove some of those walls
and ceilings to create the maze. It will have one true path,
several deadends, and no circular paths. Specifically, it uses
Wilson's algorithm.

Each chamber will have ladders in it. If a path is opened from one
chamber to the chamber above it, the ladder will be the means to
get there. Otherwise the ladder just hits a ceiling. Ladders will
always be in the northeast corner of a chamber, facing north.

The output of this program is each layer of blocks to be built.
Here is the key:
O = empty
B = block (use your block of choice, like earth or obsidian)
S = sconce (or some light that can hang)
L = ladder (or ivy) to the left of its corner
1 = signpost that reads "Start"
2 = signpost that reads "Finish"
D = cell door
The output shows each layer of the sharing stone's available space.
It could look something like this:
```
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O
O O O O O O O O O O O O O O O O O O O O O O O O


O O O O O O O O O O O O O O O O O O O O O O O O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B B B B B B B B B B B B B B B B B B B B B B O
O O B B O O O O O O O O O O O O O O O O O O O O


O O O O O O O O O O O O O O O O O O O O O O O O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B O O B O O B O O B O O B O O B O O B O O B O
O B O B B O B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B O O B O O O O O O O O O O O B O O B O O B O
O B O B B O B B B B B B B B O B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B O O O O O B O O B O O B O O B O O B O O B O
O B B B B B B B B B B B B B O B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B O O B O O B O O B O O O O O B O O B O O B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B O O B O O B O O B O O B O O B O O B O O B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B O O B O O B O O B O O B O O B O O B O O B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B O O B O O B O O B O O B O O B O O B O O B O
O B O B B B B B B B B B B B B B B B B B B B B O
O O 1 O O O O O O O O O O O O O O O O O O O O O


O O O O O O O O O O O O O O O O O O O O O O O O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B S O B S O B S O B S O B S O B S O B S O B O
O B O B B O B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B S O B S O O S O O S O O S O B S O B S O B O
O B O B B O B B B B B B B B O B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B S O O S O B S O B S O B S O B S O B S O B O
O B B B B B B B B B B B B B O B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B S O B S O B S O B S O O S O B S O B S O B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B S O B S O B S O B S O B S O B S O B S O B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B S O B S O B S O B S O B S O B S O B S O B O
O B B B B B B B B B B B B B B B B B B B B B B O
O B O L B O L B O L B O L B O L B O L B O L B O
O B S O B S O B S O B S O B S O B S O B S O B O
O B B B B B B B B B B B B B B B B B B B B B B O
O O O O O O O O O O O O O O O O O O O O O O O O
```
and so on.
"""

import random

# Referencing a block looks like this:
# blocks[height][row][column]
# where row starts at 0 and goes from west to
# east, column starts at 0 and goes from north
# to south, and height starts at 0 and goes
# from bottom to top.
num_block_rows = 24
num_block_columns = 24
num_block_layers = 16
blocks = [
    # Layer 0
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 1, Floor 0
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 2, Floor 0
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 3, Floor 0
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 4, Floor 1
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 5, Floor 1
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 6, Floor 1
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 7, Floor 2
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 8, Floor 2
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 9, Floor 2
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 10, Floor 3
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 11, Floor 3
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O', 'O', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 12, Floor 3
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O', 'L', 'B', 'O'],
        ['O', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O', 'S', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 13, Roof
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 14, Roof
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],

    # Layer 15, Roof
    [
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ],
]

# We will use a dictionary with unique string ids to
# represent the edges. An id of '012022' means the edge
# connects nodes [0, 1, 2] and [0, 2, 2].
# Each edge will be a dictionary with attributes for
# the node and the other node connecting to it, the
# blocks they would affect, whether blocks are replaced
# with ladders, and whether the edge is open or closed.
# They all start as open=False.
edges = {
    # Floor 0 west-to-east edges
    '000001': {'node': [0, 0, 0], 'other_node': [0, 0, 1], 'open': False, 'blocks': [[2, 3, 4], [3, 3, 4]], 'ladder': False},
    '001002': {'node': [0, 0, 1], 'other_node': [0, 0, 2], 'open': False, 'blocks': [[2, 3, 7], [3, 3, 7]], 'ladder': False},
    '002003': {'node': [0, 0, 2], 'other_node': [0, 0, 3], 'open': False, 'blocks': [[2, 3, 10], [3, 3, 10]], 'ladder': False},
    '003004': {'node': [0, 0, 3], 'other_node': [0, 0, 4], 'open': False, 'blocks': [[2, 3, 13], [3, 3, 13]], 'ladder': False},
    '004005': {'node': [0, 0, 4], 'other_node': [0, 0, 5], 'open': False, 'blocks': [[2, 3, 16], [3, 3, 16]], 'ladder': False},
    '005006': {'node': [0, 0, 5], 'other_node': [0, 0, 6], 'open': False, 'blocks': [[2, 3, 19], [3, 3, 19]], 'ladder': False},
    '010011': {'node': [0, 1, 0], 'other_node': [0, 1, 1], 'open': False, 'blocks': [[2, 6, 4], [3, 6, 4]], 'ladder': False},
    '011012': {'node': [0, 1, 1], 'other_node': [0, 1, 2], 'open': False, 'blocks': [[2, 6, 7], [3, 6, 7]], 'ladder': False},
    '012013': {'node': [0, 1, 2], 'other_node': [0, 1, 3], 'open': False, 'blocks': [[2, 6, 10], [3, 6, 10]], 'ladder': False},
    '013014': {'node': [0, 1, 3], 'other_node': [0, 1, 4], 'open': False, 'blocks': [[2, 6, 13], [3, 6, 13]], 'ladder': False},
    '014015': {'node': [0, 1, 4], 'other_node': [0, 1, 5], 'open': False, 'blocks': [[2, 6, 16], [3, 6, 16]], 'ladder': False},
    '015016': {'node': [0, 1, 5], 'other_node': [0, 1, 6], 'open': False, 'blocks': [[2, 6, 19], [3, 6, 19]], 'ladder': False},
    '020021': {'node': [0, 2, 0], 'other_node': [0, 2, 1], 'open': False, 'blocks': [[2, 9, 4], [3, 9, 4]], 'ladder': False},
    '021022': {'node': [0, 2, 1], 'other_node': [0, 2, 2], 'open': False, 'blocks': [[2, 9, 7], [3, 9, 7]], 'ladder': False},
    '022023': {'node': [0, 2, 2], 'other_node': [0, 2, 3], 'open': False, 'blocks': [[2, 9, 10], [3, 9, 10]], 'ladder': False},
    '023024': {'node': [0, 2, 3], 'other_node': [0, 2, 4], 'open': False, 'blocks': [[2, 9, 13], [3, 9, 13]], 'ladder': False},
    '024025': {'node': [0, 2, 4], 'other_node': [0, 2, 5], 'open': False, 'blocks': [[2, 9, 16], [3, 9, 16]], 'ladder': False},
    '025026': {'node': [0, 2, 5], 'other_node': [0, 2, 6], 'open': False, 'blocks': [[2, 9, 19], [3, 9, 19]], 'ladder': False},
    '030031': {'node': [0, 3, 0], 'other_node': [0, 3, 1], 'open': False, 'blocks': [[2, 12, 4], [3, 12, 4]], 'ladder': False},
    '031032': {'node': [0, 3, 1], 'other_node': [0, 3, 2], 'open': False, 'blocks': [[2, 12, 7], [3, 12, 7]], 'ladder': False},
    '032033': {'node': [0, 3, 2], 'other_node': [0, 3, 3], 'open': False, 'blocks': [[2, 12, 10], [3, 12, 10]], 'ladder': False},
    '033034': {'node': [0, 3, 3], 'other_node': [0, 3, 4], 'open': False, 'blocks': [[2, 12, 13], [3, 12, 13]], 'ladder': False},
    '034035': {'node': [0, 3, 4], 'other_node': [0, 3, 5], 'open': False, 'blocks': [[2, 12, 16], [3, 12, 16]], 'ladder': False},
    '035036': {'node': [0, 3, 5], 'other_node': [0, 3, 6], 'open': False, 'blocks': [[2, 12, 19], [3, 12, 19]], 'ladder': False},
    '040041': {'node': [0, 4, 0], 'other_node': [0, 4, 1], 'open': False, 'blocks': [[2, 15, 4], [3, 15, 4]], 'ladder': False},
    '041042': {'node': [0, 4, 1], 'other_node': [0, 4, 2], 'open': False, 'blocks': [[2, 15, 7], [3, 15, 7]], 'ladder': False},
    '042043': {'node': [0, 4, 2], 'other_node': [0, 4, 3], 'open': False, 'blocks': [[2, 15, 10], [3, 15, 10]], 'ladder': False},
    '043044': {'node': [0, 4, 3], 'other_node': [0, 4, 4], 'open': False, 'blocks': [[2, 15, 13], [3, 15, 13]], 'ladder': False},
    '044045': {'node': [0, 4, 4], 'other_node': [0, 4, 5], 'open': False, 'blocks': [[2, 15, 16], [3, 15, 16]], 'ladder': False},
    '045046': {'node': [0, 4, 5], 'other_node': [0, 4, 6], 'open': False, 'blocks': [[2, 15, 19], [3, 15, 19]], 'ladder': False},
    '050051': {'node': [0, 5, 0], 'other_node': [0, 5, 1], 'open': False, 'blocks': [[2, 18, 4], [3, 18, 4]], 'ladder': False},
    '051052': {'node': [0, 5, 1], 'other_node': [0, 5, 2], 'open': False, 'blocks': [[2, 18, 7], [3, 18, 7]], 'ladder': False},
    '052053': {'node': [0, 5, 2], 'other_node': [0, 5, 3], 'open': False, 'blocks': [[2, 18, 10], [3, 18, 10]], 'ladder': False},
    '053054': {'node': [0, 5, 3], 'other_node': [0, 5, 4], 'open': False, 'blocks': [[2, 18, 13], [3, 18, 13]], 'ladder': False},
    '054055': {'node': [0, 5, 4], 'other_node': [0, 5, 5], 'open': False, 'blocks': [[2, 18, 16], [3, 18, 16]], 'ladder': False},
    '055056': {'node': [0, 5, 5], 'other_node': [0, 5, 6], 'open': False, 'blocks': [[2, 18, 19], [3, 18, 19]], 'ladder': False},
    '060061': {'node': [0, 6, 0], 'other_node': [0, 6, 1], 'open': False, 'blocks': [[2, 21, 4], [3, 21, 4]], 'ladder': False},
    '061062': {'node': [0, 6, 1], 'other_node': [0, 6, 2], 'open': False, 'blocks': [[2, 21, 7], [3, 21, 7]], 'ladder': False},
    '062063': {'node': [0, 6, 2], 'other_node': [0, 6, 3], 'open': False, 'blocks': [[2, 21, 10], [3, 21, 10]], 'ladder': False},
    '063064': {'node': [0, 6, 3], 'other_node': [0, 6, 4], 'open': False, 'blocks': [[2, 21, 13], [3, 21, 13]], 'ladder': False},
    '064065': {'node': [0, 6, 4], 'other_node': [0, 6, 5], 'open': False, 'blocks': [[2, 21, 16], [3, 21, 16]], 'ladder': False},
    '065066': {'node': [0, 6, 5], 'other_node': [0, 6, 6], 'open': False, 'blocks': [[2, 21, 19], [3, 21, 19]], 'ladder': False},

    # Floor 0 north-to-south edges
    '000010': {'node': [0, 0, 0], 'other_node': [0, 1, 0], 'open': False, 'blocks': [[2, 4, 2], [3, 4, 2]], 'ladder': False},
    '010020': {'node': [0, 1, 0], 'other_node': [0, 2, 0], 'open': False, 'blocks': [[2, 7, 2], [3, 7, 2]], 'ladder': False},
    '020030': {'node': [0, 2, 0], 'other_node': [0, 3, 0], 'open': False, 'blocks': [[2, 10, 2], [3, 10, 2]], 'ladder': False},
    '030040': {'node': [0, 3, 0], 'other_node': [0, 4, 0], 'open': False, 'blocks': [[2, 13, 2], [3, 13, 2]], 'ladder': False},
    '040050': {'node': [0, 4, 0], 'other_node': [0, 5, 0], 'open': False, 'blocks': [[2, 16, 2], [3, 16, 2]], 'ladder': False},
    '050060': {'node': [0, 5, 0], 'other_node': [0, 6, 0], 'open': False, 'blocks': [[2, 19, 2], [3, 19, 2]], 'ladder': False},
    '001011': {'node': [0, 0, 1], 'other_node': [0, 1, 1], 'open': False, 'blocks': [[2, 4, 5], [3, 4, 5]], 'ladder': False},
    '011021': {'node': [0, 1, 1], 'other_node': [0, 2, 1], 'open': False, 'blocks': [[2, 7, 5], [3, 7, 5]], 'ladder': False},
    '021031': {'node': [0, 2, 1], 'other_node': [0, 3, 1], 'open': False, 'blocks': [[2, 10, 5], [3, 10, 5]], 'ladder': False},
    '031041': {'node': [0, 3, 1], 'other_node': [0, 4, 1], 'open': False, 'blocks': [[2, 13, 5], [3, 13, 5]], 'ladder': False},
    '041051': {'node': [0, 4, 1], 'other_node': [0, 5, 1], 'open': False, 'blocks': [[2, 16, 5], [3, 16, 5]], 'ladder': False},
    '051061': {'node': [0, 5, 1], 'other_node': [0, 6, 1], 'open': False, 'blocks': [[2, 19, 5], [3, 19, 5]], 'ladder': False},
    '002012': {'node': [0, 0, 2], 'other_node': [0, 1, 2], 'open': False, 'blocks': [[2, 4, 8], [3, 4, 8]], 'ladder': False},
    '012022': {'node': [0, 1, 2], 'other_node': [0, 2, 2], 'open': False, 'blocks': [[2, 7, 8], [3, 7, 8]], 'ladder': False},
    '022032': {'node': [0, 2, 2], 'other_node': [0, 3, 2], 'open': False, 'blocks': [[2, 10, 8], [3, 10, 8]], 'ladder': False},
    '032042': {'node': [0, 3, 2], 'other_node': [0, 4, 2], 'open': False, 'blocks': [[2, 13, 8], [3, 13, 8]], 'ladder': False},
    '042052': {'node': [0, 4, 2], 'other_node': [0, 5, 2], 'open': False, 'blocks': [[2, 16, 8], [3, 16, 8]], 'ladder': False},
    '052062': {'node': [0, 5, 2], 'other_node': [0, 6, 2], 'open': False, 'blocks': [[2, 19, 8], [3, 19, 8]], 'ladder': False},
    '003013': {'node': [0, 0, 3], 'other_node': [0, 1, 3], 'open': False, 'blocks': [[2, 4, 11], [3, 4, 11]], 'ladder': False},
    '013023': {'node': [0, 1, 3], 'other_node': [0, 2, 3], 'open': False, 'blocks': [[2, 7, 11], [3, 7, 11]], 'ladder': False},
    '023033': {'node': [0, 2, 3], 'other_node': [0, 3, 3], 'open': False, 'blocks': [[2, 10, 11], [3, 10, 11]], 'ladder': False},
    '033043': {'node': [0, 3, 3], 'other_node': [0, 4, 3], 'open': False, 'blocks': [[2, 13, 11], [3, 13, 11]], 'ladder': False},
    '043053': {'node': [0, 4, 3], 'other_node': [0, 5, 3], 'open': False, 'blocks': [[2, 16, 11], [3, 16, 11]], 'ladder': False},
    '053063': {'node': [0, 5, 3], 'other_node': [0, 6, 3], 'open': False, 'blocks': [[2, 19, 11], [3, 19, 11]], 'ladder': False},
    '004014': {'node': [0, 0, 4], 'other_node': [0, 1, 4], 'open': False, 'blocks': [[2, 4, 14], [3, 4, 14]], 'ladder': False},
    '014024': {'node': [0, 1, 4], 'other_node': [0, 2, 4], 'open': False, 'blocks': [[2, 7, 14], [3, 7, 14]], 'ladder': False},
    '024034': {'node': [0, 2, 4], 'other_node': [0, 3, 4], 'open': False, 'blocks': [[2, 10, 14], [3, 10, 14]], 'ladder': False},
    '034044': {'node': [0, 3, 4], 'other_node': [0, 4, 4], 'open': False, 'blocks': [[2, 13, 14], [3, 13, 14]], 'ladder': False},
    '044054': {'node': [0, 4, 4], 'other_node': [0, 5, 4], 'open': False, 'blocks': [[2, 16, 14], [3, 16, 14]], 'ladder': False},
    '054064': {'node': [0, 5, 4], 'other_node': [0, 6, 4], 'open': False, 'blocks': [[2, 19, 14], [3, 19, 14]], 'ladder': False},
    '005015': {'node': [0, 0, 5], 'other_node': [0, 1, 5], 'open': False, 'blocks': [[2, 4, 17], [3, 4, 17]], 'ladder': False},
    '015025': {'node': [0, 1, 5], 'other_node': [0, 2, 5], 'open': False, 'blocks': [[2, 7, 17], [3, 7, 17]], 'ladder': False},
    '025035': {'node': [0, 2, 5], 'other_node': [0, 3, 5], 'open': False, 'blocks': [[2, 10, 17], [3, 10, 17]], 'ladder': False},
    '035045': {'node': [0, 3, 5], 'other_node': [0, 4, 5], 'open': False, 'blocks': [[2, 13, 17], [3, 13, 17]], 'ladder': False},
    '045055': {'node': [0, 4, 5], 'other_node': [0, 5, 5], 'open': False, 'blocks': [[2, 16, 17], [3, 16, 17]], 'ladder': False},
    '055065': {'node': [0, 5, 5], 'other_node': [0, 6, 5], 'open': False, 'blocks': [[2, 19, 17], [3, 19, 17]], 'ladder': False},
    '006016': {'node': [0, 0, 6], 'other_node': [0, 1, 6], 'open': False, 'blocks': [[2, 4, 20], [3, 4, 20]], 'ladder': False},
    '016026': {'node': [0, 1, 6], 'other_node': [0, 2, 6], 'open': False, 'blocks': [[2, 7, 20], [3, 7, 20]], 'ladder': False},
    '026036': {'node': [0, 2, 6], 'other_node': [0, 3, 6], 'open': False, 'blocks': [[2, 10, 20], [3, 10, 20]], 'ladder': False},
    '036046': {'node': [0, 3, 6], 'other_node': [0, 4, 6], 'open': False, 'blocks': [[2, 13, 20], [3, 13, 20]], 'ladder': False},
    '046056': {'node': [0, 4, 6], 'other_node': [0, 5, 6], 'open': False, 'blocks': [[2, 16, 20], [3, 16, 20]], 'ladder': False},
    '056066': {'node': [0, 5, 6], 'other_node': [0, 6, 6], 'open': False, 'blocks': [[2, 19, 20], [3, 19, 20]], 'ladder': False},

    # Floor 1 bottom-to-top edges
    '000100': {'node': [0, 0, 0], 'other_node': [1, 0, 0], 'open': False, 'blocks': [[4, 2, 3]], 'ladder': True},
    '001101': {'node': [0, 0, 1], 'other_node': [1, 0, 1], 'open': False, 'blocks': [[4, 2, 6]], 'ladder': True},
    '002102': {'node': [0, 0, 2], 'other_node': [1, 0, 2], 'open': False, 'blocks': [[4, 2, 9]], 'ladder': True},
    '003103': {'node': [0, 0, 3], 'other_node': [1, 0, 3], 'open': False, 'blocks': [[4, 2, 12]], 'ladder': True},
    '004104': {'node': [0, 0, 4], 'other_node': [1, 0, 4], 'open': False, 'blocks': [[4, 2, 15]], 'ladder': True},
    '005105': {'node': [0, 0, 5], 'other_node': [1, 0, 5], 'open': False, 'blocks': [[4, 2, 18]], 'ladder': True},
    '006106': {'node': [0, 0, 6], 'other_node': [1, 0, 6], 'open': False, 'blocks': [[4, 2, 21]], 'ladder': True},
    '010110': {'node': [0, 1, 0], 'other_node': [1, 1, 0], 'open': False, 'blocks': [[4, 5, 3]], 'ladder': True},
    '011111': {'node': [0, 1, 1], 'other_node': [1, 1, 1], 'open': False, 'blocks': [[4, 5, 6]], 'ladder': True},
    '012112': {'node': [0, 1, 2], 'other_node': [1, 1, 2], 'open': False, 'blocks': [[4, 5, 9]], 'ladder': True},
    '013113': {'node': [0, 1, 3], 'other_node': [1, 1, 3], 'open': False, 'blocks': [[4, 5, 12]], 'ladder': True},
    '014114': {'node': [0, 1, 4], 'other_node': [1, 1, 4], 'open': False, 'blocks': [[4, 5, 15]], 'ladder': True},
    '015115': {'node': [0, 1, 5], 'other_node': [1, 1, 5], 'open': False, 'blocks': [[4, 5, 18]], 'ladder': True},
    '016116': {'node': [0, 1, 6], 'other_node': [1, 1, 6], 'open': False, 'blocks': [[4, 5, 21]], 'ladder': True},
    '020120': {'node': [0, 2, 0], 'other_node': [1, 2, 0], 'open': False, 'blocks': [[4, 8, 3]], 'ladder': True},
    '021121': {'node': [0, 2, 1], 'other_node': [1, 2, 1], 'open': False, 'blocks': [[4, 8, 6]], 'ladder': True},
    '022122': {'node': [0, 2, 2], 'other_node': [1, 2, 2], 'open': False, 'blocks': [[4, 8, 9]], 'ladder': True},
    '023123': {'node': [0, 2, 3], 'other_node': [1, 2, 3], 'open': False, 'blocks': [[4, 8, 12]], 'ladder': True},
    '024124': {'node': [0, 2, 4], 'other_node': [1, 2, 4], 'open': False, 'blocks': [[4, 8, 15]], 'ladder': True},
    '025125': {'node': [0, 2, 5], 'other_node': [1, 2, 5], 'open': False, 'blocks': [[4, 8, 18]], 'ladder': True},
    '026126': {'node': [0, 2, 6], 'other_node': [1, 2, 6], 'open': False, 'blocks': [[4, 8, 21]], 'ladder': True},
    '030130': {'node': [0, 3, 0], 'other_node': [1, 3, 0], 'open': False, 'blocks': [[4, 11, 3]], 'ladder': True},
    '031131': {'node': [0, 3, 1], 'other_node': [1, 3, 1], 'open': False, 'blocks': [[4, 11, 6]], 'ladder': True},
    '032132': {'node': [0, 3, 2], 'other_node': [1, 3, 2], 'open': False, 'blocks': [[4, 11, 9]], 'ladder': True},
    '033133': {'node': [0, 3, 3], 'other_node': [1, 3, 3], 'open': False, 'blocks': [[4, 11, 12]], 'ladder': True},
    '034134': {'node': [0, 3, 4], 'other_node': [1, 3, 4], 'open': False, 'blocks': [[4, 11, 15]], 'ladder': True},
    '035135': {'node': [0, 3, 5], 'other_node': [1, 3, 5], 'open': False, 'blocks': [[4, 11, 18]], 'ladder': True},
    '036136': {'node': [0, 3, 6], 'other_node': [1, 3, 6], 'open': False, 'blocks': [[4, 11, 21]], 'ladder': True},
    '040140': {'node': [0, 4, 0], 'other_node': [1, 4, 0], 'open': False, 'blocks': [[4, 14, 3]], 'ladder': True},
    '041141': {'node': [0, 4, 1], 'other_node': [1, 4, 1], 'open': False, 'blocks': [[4, 14, 6]], 'ladder': True},
    '042142': {'node': [0, 4, 2], 'other_node': [1, 4, 2], 'open': False, 'blocks': [[4, 14, 9]], 'ladder': True},
    '043143': {'node': [0, 4, 3], 'other_node': [1, 4, 3], 'open': False, 'blocks': [[4, 14, 12]], 'ladder': True},
    '044144': {'node': [0, 4, 4], 'other_node': [1, 4, 4], 'open': False, 'blocks': [[4, 14, 15]], 'ladder': True},
    '045145': {'node': [0, 4, 5], 'other_node': [1, 4, 5], 'open': False, 'blocks': [[4, 14, 18]], 'ladder': True},
    '046146': {'node': [0, 4, 6], 'other_node': [1, 4, 6], 'open': False, 'blocks': [[4, 14, 21]], 'ladder': True},
    '050150': {'node': [0, 5, 0], 'other_node': [1, 5, 0], 'open': False, 'blocks': [[4, 17, 3]], 'ladder': True},
    '051151': {'node': [0, 5, 1], 'other_node': [1, 5, 1], 'open': False, 'blocks': [[4, 17, 6]], 'ladder': True},
    '052152': {'node': [0, 5, 2], 'other_node': [1, 5, 2], 'open': False, 'blocks': [[4, 17, 9]], 'ladder': True},
    '053153': {'node': [0, 5, 3], 'other_node': [1, 5, 3], 'open': False, 'blocks': [[4, 17, 12]], 'ladder': True},
    '054154': {'node': [0, 5, 4], 'other_node': [1, 5, 4], 'open': False, 'blocks': [[4, 17, 15]], 'ladder': True},
    '055155': {'node': [0, 5, 5], 'other_node': [1, 5, 5], 'open': False, 'blocks': [[4, 17, 18]], 'ladder': True},
    '056156': {'node': [0, 5, 6], 'other_node': [1, 5, 6], 'open': False, 'blocks': [[4, 17, 21]], 'ladder': True},
    '060160': {'node': [0, 6, 0], 'other_node': [1, 6, 0], 'open': False, 'blocks': [[4, 20, 3]], 'ladder': True},
    '061161': {'node': [0, 6, 1], 'other_node': [1, 6, 1], 'open': False, 'blocks': [[4, 20, 6]], 'ladder': True},
    '062162': {'node': [0, 6, 2], 'other_node': [1, 6, 2], 'open': False, 'blocks': [[4, 20, 9]], 'ladder': True},
    '063163': {'node': [0, 6, 3], 'other_node': [1, 6, 3], 'open': False, 'blocks': [[4, 20, 12]], 'ladder': True},
    '064164': {'node': [0, 6, 4], 'other_node': [1, 6, 4], 'open': False, 'blocks': [[4, 20, 15]], 'ladder': True},
    '065165': {'node': [0, 6, 5], 'other_node': [1, 6, 5], 'open': False, 'blocks': [[4, 20, 18]], 'ladder': True},
    '066166': {'node': [0, 6, 6], 'other_node': [1, 6, 6], 'open': False, 'blocks': [[4, 20, 21]], 'ladder': True},
    
    # Floor 1 west-to-east edges
    '100101': {'node': [1, 0, 0], 'other_node': [1, 0, 1], 'open': False, 'blocks': [[5, 3, 4], [6, 3, 4]], 'ladder': False},
    '101102': {'node': [1, 0, 1], 'other_node': [1, 0, 2], 'open': False, 'blocks': [[5, 3, 7], [6, 3, 7]], 'ladder': False},
    '102103': {'node': [1, 0, 2], 'other_node': [1, 0, 3], 'open': False, 'blocks': [[5, 3, 10], [6, 3, 10]], 'ladder': False},
    '103104': {'node': [1, 0, 3], 'other_node': [1, 0, 4], 'open': False, 'blocks': [[5, 3, 13], [6, 3, 13]], 'ladder': False},
    '104105': {'node': [1, 0, 4], 'other_node': [1, 0, 5], 'open': False, 'blocks': [[5, 3, 16], [6, 3, 16]], 'ladder': False},
    '105106': {'node': [1, 0, 5], 'other_node': [1, 0, 6], 'open': False, 'blocks': [[5, 3, 19], [6, 3, 19]], 'ladder': False},
    '110111': {'node': [1, 1, 0], 'other_node': [1, 1, 1], 'open': False, 'blocks': [[5, 6, 4], [6, 6, 4]], 'ladder': False},
    '111112': {'node': [1, 1, 1], 'other_node': [1, 1, 2], 'open': False, 'blocks': [[5, 6, 7], [6, 6, 7]], 'ladder': False},
    '112113': {'node': [1, 1, 2], 'other_node': [1, 1, 3], 'open': False, 'blocks': [[5, 6, 10], [6, 6, 10]], 'ladder': False},
    '113114': {'node': [1, 1, 3], 'other_node': [1, 1, 4], 'open': False, 'blocks': [[5, 6, 13], [6, 6, 13]], 'ladder': False},
    '114115': {'node': [1, 1, 4], 'other_node': [1, 1, 5], 'open': False, 'blocks': [[5, 6, 16], [6, 6, 16]], 'ladder': False},
    '115116': {'node': [1, 1, 5], 'other_node': [1, 1, 6], 'open': False, 'blocks': [[5, 6, 19], [6, 6, 19]], 'ladder': False},
    '120121': {'node': [1, 2, 0], 'other_node': [1, 2, 1], 'open': False, 'blocks': [[5, 9, 4], [6, 9, 4]], 'ladder': False},
    '121122': {'node': [1, 2, 1], 'other_node': [1, 2, 2], 'open': False, 'blocks': [[5, 9, 7], [6, 9, 7]], 'ladder': False},
    '122123': {'node': [1, 2, 2], 'other_node': [1, 2, 3], 'open': False, 'blocks': [[5, 9, 10], [6, 9, 10]], 'ladder': False},
    '123124': {'node': [1, 2, 3], 'other_node': [1, 2, 4], 'open': False, 'blocks': [[5, 9, 13], [6, 9, 13]], 'ladder': False},
    '124125': {'node': [1, 2, 4], 'other_node': [1, 2, 5], 'open': False, 'blocks': [[5, 9, 16], [6, 9, 16]], 'ladder': False},
    '125126': {'node': [1, 2, 5], 'other_node': [1, 2, 6], 'open': False, 'blocks': [[5, 9, 19], [6, 9, 19]], 'ladder': False},
    '130131': {'node': [1, 3, 0], 'other_node': [1, 3, 1], 'open': False, 'blocks': [[5, 12, 4], [6, 12, 4]], 'ladder': False},
    '131132': {'node': [1, 3, 1], 'other_node': [1, 3, 2], 'open': False, 'blocks': [[5, 12, 7], [6, 12, 7]], 'ladder': False},
    '132133': {'node': [1, 3, 2], 'other_node': [1, 3, 3], 'open': False, 'blocks': [[5, 12, 10], [6, 12, 10]], 'ladder': False},
    '133134': {'node': [1, 3, 3], 'other_node': [1, 3, 4], 'open': False, 'blocks': [[5, 12, 13], [6, 12, 13]], 'ladder': False},
    '134135': {'node': [1, 3, 4], 'other_node': [1, 3, 5], 'open': False, 'blocks': [[5, 12, 16], [6, 12, 16]], 'ladder': False},
    '135136': {'node': [1, 3, 5], 'other_node': [1, 3, 6], 'open': False, 'blocks': [[5, 12, 19], [6, 12, 19]], 'ladder': False},
    '140141': {'node': [1, 4, 0], 'other_node': [1, 4, 1], 'open': False, 'blocks': [[5, 15, 4], [6, 15, 4]], 'ladder': False},
    '141142': {'node': [1, 4, 1], 'other_node': [1, 4, 2], 'open': False, 'blocks': [[5, 15, 7], [6, 15, 7]], 'ladder': False},
    '142143': {'node': [1, 4, 2], 'other_node': [1, 4, 3], 'open': False, 'blocks': [[5, 15, 10], [6, 15, 10]], 'ladder': False},
    '143144': {'node': [1, 4, 3], 'other_node': [1, 4, 4], 'open': False, 'blocks': [[5, 15, 13], [6, 15, 13]], 'ladder': False},
    '144145': {'node': [1, 4, 4], 'other_node': [1, 4, 5], 'open': False, 'blocks': [[5, 15, 16], [6, 15, 16]], 'ladder': False},
    '145146': {'node': [1, 4, 5], 'other_node': [1, 4, 6], 'open': False, 'blocks': [[5, 15, 19], [6, 15, 19]], 'ladder': False},
    '150151': {'node': [1, 5, 0], 'other_node': [1, 5, 1], 'open': False, 'blocks': [[5, 18, 4], [6, 18, 4]], 'ladder': False},
    '151152': {'node': [1, 5, 1], 'other_node': [1, 5, 2], 'open': False, 'blocks': [[5, 18, 7], [6, 18, 7]], 'ladder': False},
    '152153': {'node': [1, 5, 2], 'other_node': [1, 5, 3], 'open': False, 'blocks': [[5, 18, 10], [6, 18, 10]], 'ladder': False},
    '153154': {'node': [1, 5, 3], 'other_node': [1, 5, 4], 'open': False, 'blocks': [[5, 18, 13], [6, 18, 13]], 'ladder': False},
    '154155': {'node': [1, 5, 4], 'other_node': [1, 5, 5], 'open': False, 'blocks': [[5, 18, 16], [6, 18, 16]], 'ladder': False},
    '155156': {'node': [1, 5, 5], 'other_node': [1, 5, 6], 'open': False, 'blocks': [[5, 18, 19], [6, 18, 19]], 'ladder': False},
    '160161': {'node': [1, 6, 0], 'other_node': [1, 6, 1], 'open': False, 'blocks': [[5, 21, 4], [6, 21, 4]], 'ladder': False},
    '161162': {'node': [1, 6, 1], 'other_node': [1, 6, 2], 'open': False, 'blocks': [[5, 21, 7], [6, 21, 7]], 'ladder': False},
    '162163': {'node': [1, 6, 2], 'other_node': [1, 6, 3], 'open': False, 'blocks': [[5, 21, 10], [6, 21, 10]], 'ladder': False},
    '163164': {'node': [1, 6, 3], 'other_node': [1, 6, 4], 'open': False, 'blocks': [[5, 21, 13], [6, 21, 13]], 'ladder': False},
    '164165': {'node': [1, 6, 4], 'other_node': [1, 6, 5], 'open': False, 'blocks': [[5, 21, 16], [6, 21, 16]], 'ladder': False},
    '165166': {'node': [1, 6, 5], 'other_node': [1, 6, 6], 'open': False, 'blocks': [[5, 21, 19], [6, 21, 19]], 'ladder': False},

    # Floor 1 north-to-south edges
    '100110': {'node': [1, 0, 0], 'other_node': [1, 1, 0], 'open': False, 'blocks': [[5, 4, 2], [6, 4, 2]], 'ladder': False},
    '110120': {'node': [1, 1, 0], 'other_node': [1, 2, 0], 'open': False, 'blocks': [[5, 7, 2], [6, 7, 2]], 'ladder': False},
    '120130': {'node': [1, 2, 0], 'other_node': [1, 3, 0], 'open': False, 'blocks': [[5, 10, 2], [6, 10, 2]], 'ladder': False},
    '130140': {'node': [1, 3, 0], 'other_node': [1, 4, 0], 'open': False, 'blocks': [[5, 13, 2], [6, 13, 2]], 'ladder': False},
    '140150': {'node': [1, 4, 0], 'other_node': [1, 5, 0], 'open': False, 'blocks': [[5, 16, 2], [6, 16, 2]], 'ladder': False},
    '150160': {'node': [1, 5, 0], 'other_node': [1, 6, 0], 'open': False, 'blocks': [[5, 19, 2], [6, 19, 2]], 'ladder': False},
    '101111': {'node': [1, 0, 1], 'other_node': [1, 1, 1], 'open': False, 'blocks': [[5, 4, 5], [6, 4, 5]], 'ladder': False},
    '111121': {'node': [1, 1, 1], 'other_node': [1, 2, 1], 'open': False, 'blocks': [[5, 7, 5], [6, 7, 5]], 'ladder': False},
    '121131': {'node': [1, 2, 1], 'other_node': [1, 3, 1], 'open': False, 'blocks': [[5, 10, 5], [6, 10, 5]], 'ladder': False},
    '131141': {'node': [1, 3, 1], 'other_node': [1, 4, 1], 'open': False, 'blocks': [[5, 13, 5], [6, 13, 5]], 'ladder': False},
    '141151': {'node': [1, 4, 1], 'other_node': [1, 5, 1], 'open': False, 'blocks': [[5, 16, 5], [6, 16, 5]], 'ladder': False},
    '151161': {'node': [1, 5, 1], 'other_node': [1, 6, 1], 'open': False, 'blocks': [[5, 19, 5], [6, 19, 5]], 'ladder': False},
    '102112': {'node': [1, 0, 2], 'other_node': [1, 1, 2], 'open': False, 'blocks': [[5, 4, 8], [6, 4, 8]], 'ladder': False},
    '112122': {'node': [1, 1, 2], 'other_node': [1, 2, 2], 'open': False, 'blocks': [[5, 7, 8], [6, 7, 8]], 'ladder': False},
    '122132': {'node': [1, 2, 2], 'other_node': [1, 3, 2], 'open': False, 'blocks': [[5, 10, 8], [6, 10, 8]], 'ladder': False},
    '132142': {'node': [1, 3, 2], 'other_node': [1, 4, 2], 'open': False, 'blocks': [[5, 13, 8], [6, 13, 8]], 'ladder': False},
    '142152': {'node': [1, 4, 2], 'other_node': [1, 5, 2], 'open': False, 'blocks': [[5, 16, 8], [6, 16, 8]], 'ladder': False},
    '152162': {'node': [1, 5, 2], 'other_node': [1, 6, 2], 'open': False, 'blocks': [[5, 19, 8], [6, 19, 8]], 'ladder': False},
    '103113': {'node': [1, 0, 3], 'other_node': [1, 1, 3], 'open': False, 'blocks': [[5, 4, 11], [6, 4, 11]], 'ladder': False},
    '113123': {'node': [1, 1, 3], 'other_node': [1, 2, 3], 'open': False, 'blocks': [[5, 7, 11], [6, 7, 11]], 'ladder': False},
    '123133': {'node': [1, 2, 3], 'other_node': [1, 3, 3], 'open': False, 'blocks': [[5, 10, 11], [6, 10, 11]], 'ladder': False},
    '133143': {'node': [1, 3, 3], 'other_node': [1, 4, 3], 'open': False, 'blocks': [[5, 13, 11], [6, 13, 11]], 'ladder': False},
    '143153': {'node': [1, 4, 3], 'other_node': [1, 5, 3], 'open': False, 'blocks': [[5, 16, 11], [6, 16, 11]], 'ladder': False},
    '153163': {'node': [1, 5, 3], 'other_node': [1, 6, 3], 'open': False, 'blocks': [[5, 19, 11], [6, 19, 11]], 'ladder': False},
    '104114': {'node': [1, 0, 4], 'other_node': [1, 1, 4], 'open': False, 'blocks': [[5, 4, 14], [6, 4, 14]], 'ladder': False},
    '114124': {'node': [1, 1, 4], 'other_node': [1, 2, 4], 'open': False, 'blocks': [[5, 7, 14], [6, 7, 14]], 'ladder': False},
    '124134': {'node': [1, 2, 4], 'other_node': [1, 3, 4], 'open': False, 'blocks': [[5, 10, 14], [6, 10, 14]], 'ladder': False},
    '134144': {'node': [1, 3, 4], 'other_node': [1, 4, 4], 'open': False, 'blocks': [[5, 13, 14], [6, 13, 14]], 'ladder': False},
    '144154': {'node': [1, 4, 4], 'other_node': [1, 5, 4], 'open': False, 'blocks': [[5, 16, 14], [6, 16, 14]], 'ladder': False},
    '154164': {'node': [1, 5, 4], 'other_node': [1, 6, 4], 'open': False, 'blocks': [[5, 19, 14], [6, 19, 14]], 'ladder': False},
    '105115': {'node': [1, 0, 5], 'other_node': [1, 1, 5], 'open': False, 'blocks': [[5, 4, 17], [6, 4, 17]], 'ladder': False},
    '115125': {'node': [1, 1, 5], 'other_node': [1, 2, 5], 'open': False, 'blocks': [[5, 7, 17], [6, 7, 17]], 'ladder': False},
    '125135': {'node': [1, 2, 5], 'other_node': [1, 3, 5], 'open': False, 'blocks': [[5, 10, 17], [6, 10, 17]], 'ladder': False},
    '135145': {'node': [1, 3, 5], 'other_node': [1, 4, 5], 'open': False, 'blocks': [[5, 13, 17], [6, 13, 17]], 'ladder': False},
    '145155': {'node': [1, 4, 5], 'other_node': [1, 5, 5], 'open': False, 'blocks': [[5, 16, 17], [6, 16, 17]], 'ladder': False},
    '155165': {'node': [1, 5, 5], 'other_node': [1, 6, 5], 'open': False, 'blocks': [[5, 19, 17], [6, 19, 17]], 'ladder': False},
    '106116': {'node': [1, 0, 6], 'other_node': [1, 1, 6], 'open': False, 'blocks': [[5, 4, 20], [6, 4, 20]], 'ladder': False},
    '116126': {'node': [1, 1, 6], 'other_node': [1, 2, 6], 'open': False, 'blocks': [[5, 7, 20], [6, 7, 20]], 'ladder': False},
    '126136': {'node': [1, 2, 6], 'other_node': [1, 3, 6], 'open': False, 'blocks': [[5, 10, 20], [6, 10, 20]], 'ladder': False},
    '136146': {'node': [1, 3, 6], 'other_node': [1, 4, 6], 'open': False, 'blocks': [[5, 13, 20], [6, 13, 20]], 'ladder': False},
    '146156': {'node': [1, 4, 6], 'other_node': [1, 5, 6], 'open': False, 'blocks': [[5, 16, 20], [6, 16, 20]], 'ladder': False},
    '156166': {'node': [1, 5, 6], 'other_node': [1, 6, 6], 'open': False, 'blocks': [[5, 19, 20], [6, 19, 20]], 'ladder': False},

    # Floor 2 bottom-to-top edges
    '100200': {'node': [1, 0, 0], 'other_node': [2, 0, 0], 'open': False, 'blocks': [[7, 2, 3]], 'ladder': True},
    '101201': {'node': [1, 0, 1], 'other_node': [2, 0, 1], 'open': False, 'blocks': [[7, 2, 6]], 'ladder': True},
    '102202': {'node': [1, 0, 2], 'other_node': [2, 0, 2], 'open': False, 'blocks': [[7, 2, 9]], 'ladder': True},
    '103203': {'node': [1, 0, 3], 'other_node': [2, 0, 3], 'open': False, 'blocks': [[7, 2, 12]], 'ladder': True},
    '104204': {'node': [1, 0, 4], 'other_node': [2, 0, 4], 'open': False, 'blocks': [[7, 2, 15]], 'ladder': True},
    '105205': {'node': [1, 0, 5], 'other_node': [2, 0, 5], 'open': False, 'blocks': [[7, 2, 18]], 'ladder': True},
    '106206': {'node': [1, 0, 6], 'other_node': [2, 0, 6], 'open': False, 'blocks': [[7, 2, 21]], 'ladder': True},
    '110210': {'node': [1, 1, 0], 'other_node': [2, 1, 0], 'open': False, 'blocks': [[7, 5, 3]], 'ladder': True},
    '111211': {'node': [1, 1, 1], 'other_node': [2, 1, 1], 'open': False, 'blocks': [[7, 5, 6]], 'ladder': True},
    '112212': {'node': [1, 1, 2], 'other_node': [2, 1, 2], 'open': False, 'blocks': [[7, 5, 9]], 'ladder': True},
    '113213': {'node': [1, 1, 3], 'other_node': [2, 1, 3], 'open': False, 'blocks': [[7, 5, 12]], 'ladder': True},
    '114214': {'node': [1, 1, 4], 'other_node': [2, 1, 4], 'open': False, 'blocks': [[7, 5, 15]], 'ladder': True},
    '115215': {'node': [1, 1, 5], 'other_node': [2, 1, 5], 'open': False, 'blocks': [[7, 5, 18]], 'ladder': True},
    '116216': {'node': [1, 1, 6], 'other_node': [2, 1, 6], 'open': False, 'blocks': [[7, 5, 21]], 'ladder': True},
    '120220': {'node': [1, 2, 0], 'other_node': [2, 2, 0], 'open': False, 'blocks': [[7, 8, 3]], 'ladder': True},
    '121221': {'node': [1, 2, 1], 'other_node': [2, 2, 1], 'open': False, 'blocks': [[7, 8, 6]], 'ladder': True},
    '122222': {'node': [1, 2, 2], 'other_node': [2, 2, 2], 'open': False, 'blocks': [[7, 8, 9]], 'ladder': True},
    '123223': {'node': [1, 2, 3], 'other_node': [2, 2, 3], 'open': False, 'blocks': [[7, 8, 12]], 'ladder': True},
    '124224': {'node': [1, 2, 4], 'other_node': [2, 2, 4], 'open': False, 'blocks': [[7, 8, 15]], 'ladder': True},
    '125225': {'node': [1, 2, 5], 'other_node': [2, 2, 5], 'open': False, 'blocks': [[7, 8, 18]], 'ladder': True},
    '126226': {'node': [1, 2, 6], 'other_node': [2, 2, 6], 'open': False, 'blocks': [[7, 8, 21]], 'ladder': True},
    '130230': {'node': [1, 3, 0], 'other_node': [2, 3, 0], 'open': False, 'blocks': [[7, 11, 3]], 'ladder': True},
    '131231': {'node': [1, 3, 1], 'other_node': [2, 3, 1], 'open': False, 'blocks': [[7, 11, 6]], 'ladder': True},
    '132232': {'node': [1, 3, 2], 'other_node': [2, 3, 2], 'open': False, 'blocks': [[7, 11, 9]], 'ladder': True},
    '133233': {'node': [1, 3, 3], 'other_node': [2, 3, 3], 'open': False, 'blocks': [[7, 11, 12]], 'ladder': True},
    '134234': {'node': [1, 3, 4], 'other_node': [2, 3, 4], 'open': False, 'blocks': [[7, 11, 15]], 'ladder': True},
    '135235': {'node': [1, 3, 5], 'other_node': [2, 3, 5], 'open': False, 'blocks': [[7, 11, 18]], 'ladder': True},
    '136236': {'node': [1, 3, 6], 'other_node': [2, 3, 6], 'open': False, 'blocks': [[7, 11, 21]], 'ladder': True},
    '140240': {'node': [1, 4, 0], 'other_node': [2, 4, 0], 'open': False, 'blocks': [[7, 14, 3]], 'ladder': True},
    '141241': {'node': [1, 4, 1], 'other_node': [2, 4, 1], 'open': False, 'blocks': [[7, 14, 6]], 'ladder': True},
    '142242': {'node': [1, 4, 2], 'other_node': [2, 4, 2], 'open': False, 'blocks': [[7, 14, 9]], 'ladder': True},
    '143243': {'node': [1, 4, 3], 'other_node': [2, 4, 3], 'open': False, 'blocks': [[7, 14, 12]], 'ladder': True},
    '144244': {'node': [1, 4, 4], 'other_node': [2, 4, 4], 'open': False, 'blocks': [[7, 14, 15]], 'ladder': True},
    '145245': {'node': [1, 4, 5], 'other_node': [2, 4, 5], 'open': False, 'blocks': [[7, 14, 18]], 'ladder': True},
    '146246': {'node': [1, 4, 6], 'other_node': [2, 4, 6], 'open': False, 'blocks': [[7, 14, 21]], 'ladder': True},
    '150250': {'node': [1, 5, 0], 'other_node': [2, 5, 0], 'open': False, 'blocks': [[7, 17, 3]], 'ladder': True},
    '151251': {'node': [1, 5, 1], 'other_node': [2, 5, 1], 'open': False, 'blocks': [[7, 17, 6]], 'ladder': True},
    '152252': {'node': [1, 5, 2], 'other_node': [2, 5, 2], 'open': False, 'blocks': [[7, 17, 9]], 'ladder': True},
    '153253': {'node': [1, 5, 3], 'other_node': [2, 5, 3], 'open': False, 'blocks': [[7, 17, 12]], 'ladder': True},
    '154254': {'node': [1, 5, 4], 'other_node': [2, 5, 4], 'open': False, 'blocks': [[7, 17, 15]], 'ladder': True},
    '155255': {'node': [1, 5, 5], 'other_node': [2, 5, 5], 'open': False, 'blocks': [[7, 17, 18]], 'ladder': True},
    '156256': {'node': [1, 5, 6], 'other_node': [2, 5, 6], 'open': False, 'blocks': [[7, 17, 21]], 'ladder': True},
    '160260': {'node': [1, 6, 0], 'other_node': [2, 6, 0], 'open': False, 'blocks': [[7, 20, 3]], 'ladder': True},
    '161261': {'node': [1, 6, 1], 'other_node': [2, 6, 1], 'open': False, 'blocks': [[7, 20, 6]], 'ladder': True},
    '162262': {'node': [1, 6, 2], 'other_node': [2, 6, 2], 'open': False, 'blocks': [[7, 20, 9]], 'ladder': True},
    '163263': {'node': [1, 6, 3], 'other_node': [2, 6, 3], 'open': False, 'blocks': [[7, 20, 12]], 'ladder': True},
    '164264': {'node': [1, 6, 4], 'other_node': [2, 6, 4], 'open': False, 'blocks': [[7, 20, 15]], 'ladder': True},
    '165265': {'node': [1, 6, 5], 'other_node': [2, 6, 5], 'open': False, 'blocks': [[7, 20, 18]], 'ladder': True},
    '166266': {'node': [1, 6, 6], 'other_node': [2, 6, 6], 'open': False, 'blocks': [[7, 20, 21]], 'ladder': True},
    
    # Floor 2 west-to-east edges
    '200201': {'node': [2, 0, 0], 'other_node': [2, 0, 1], 'open': False, 'blocks': [[8, 3, 4], [9, 3, 4]], 'ladder': False},
    '201202': {'node': [2, 0, 1], 'other_node': [2, 0, 2], 'open': False, 'blocks': [[8, 3, 7], [9, 3, 7]], 'ladder': False},
    '202203': {'node': [2, 0, 2], 'other_node': [2, 0, 3], 'open': False, 'blocks': [[8, 3, 10], [9, 3, 10]], 'ladder': False},
    '203204': {'node': [2, 0, 3], 'other_node': [2, 0, 4], 'open': False, 'blocks': [[8, 3, 13], [9, 3, 13]], 'ladder': False},
    '204205': {'node': [2, 0, 4], 'other_node': [2, 0, 5], 'open': False, 'blocks': [[8, 3, 16], [9, 3, 16]], 'ladder': False},
    '205206': {'node': [2, 0, 5], 'other_node': [2, 0, 6], 'open': False, 'blocks': [[8, 3, 19], [9, 3, 19]], 'ladder': False},
    '210211': {'node': [2, 1, 0], 'other_node': [2, 1, 1], 'open': False, 'blocks': [[8, 6, 4], [9, 6, 4]], 'ladder': False},
    '211212': {'node': [2, 1, 1], 'other_node': [2, 1, 2], 'open': False, 'blocks': [[8, 6, 7], [9, 6, 7]], 'ladder': False},
    '212213': {'node': [2, 1, 2], 'other_node': [2, 1, 3], 'open': False, 'blocks': [[8, 6, 10], [9, 6, 10]], 'ladder': False},
    '213214': {'node': [2, 1, 3], 'other_node': [2, 1, 4], 'open': False, 'blocks': [[8, 6, 13], [9, 6, 13]], 'ladder': False},
    '214215': {'node': [2, 1, 4], 'other_node': [2, 1, 5], 'open': False, 'blocks': [[8, 6, 16], [9, 6, 16]], 'ladder': False},
    '215216': {'node': [2, 1, 5], 'other_node': [2, 1, 6], 'open': False, 'blocks': [[8, 6, 19], [9, 6, 19]], 'ladder': False},
    '220221': {'node': [2, 2, 0], 'other_node': [2, 2, 1], 'open': False, 'blocks': [[8, 9, 4], [9, 9, 4]], 'ladder': False},
    '221222': {'node': [2, 2, 1], 'other_node': [2, 2, 2], 'open': False, 'blocks': [[8, 9, 7], [9, 9, 7]], 'ladder': False},
    '222223': {'node': [2, 2, 2], 'other_node': [2, 2, 3], 'open': False, 'blocks': [[8, 9, 10], [9, 9, 10]], 'ladder': False},
    '223224': {'node': [2, 2, 3], 'other_node': [2, 2, 4], 'open': False, 'blocks': [[8, 9, 13], [9, 9, 13]], 'ladder': False},
    '224225': {'node': [2, 2, 4], 'other_node': [2, 2, 5], 'open': False, 'blocks': [[8, 9, 16], [9, 9, 16]], 'ladder': False},
    '225226': {'node': [2, 2, 5], 'other_node': [2, 2, 6], 'open': False, 'blocks': [[8, 9, 19], [9, 9, 19]], 'ladder': False},
    '230231': {'node': [2, 3, 0], 'other_node': [2, 3, 1], 'open': False, 'blocks': [[8, 12, 4], [9, 12, 4]], 'ladder': False},
    '231232': {'node': [2, 3, 1], 'other_node': [2, 3, 2], 'open': False, 'blocks': [[8, 12, 7], [9, 12, 7]], 'ladder': False},
    '232233': {'node': [2, 3, 2], 'other_node': [2, 3, 3], 'open': False, 'blocks': [[8, 12, 10], [9, 12, 10]], 'ladder': False},
    '233234': {'node': [2, 3, 3], 'other_node': [2, 3, 4], 'open': False, 'blocks': [[8, 12, 13], [9, 12, 13]], 'ladder': False},
    '234235': {'node': [2, 3, 4], 'other_node': [2, 3, 5], 'open': False, 'blocks': [[8, 12, 16], [9, 12, 16]], 'ladder': False},
    '235236': {'node': [2, 3, 5], 'other_node': [2, 3, 6], 'open': False, 'blocks': [[8, 12, 19], [9, 12, 19]], 'ladder': False},
    '240241': {'node': [2, 4, 0], 'other_node': [2, 4, 1], 'open': False, 'blocks': [[8, 15, 4], [9, 15, 4]], 'ladder': False},
    '241242': {'node': [2, 4, 1], 'other_node': [2, 4, 2], 'open': False, 'blocks': [[8, 15, 7], [9, 15, 7]], 'ladder': False},
    '242243': {'node': [2, 4, 2], 'other_node': [2, 4, 3], 'open': False, 'blocks': [[8, 15, 10], [9, 15, 10]], 'ladder': False},
    '243244': {'node': [2, 4, 3], 'other_node': [2, 4, 4], 'open': False, 'blocks': [[8, 15, 13], [9, 15, 13]], 'ladder': False},
    '244245': {'node': [2, 4, 4], 'other_node': [2, 4, 5], 'open': False, 'blocks': [[8, 15, 16], [9, 15, 16]], 'ladder': False},
    '245246': {'node': [2, 4, 5], 'other_node': [2, 4, 6], 'open': False, 'blocks': [[8, 15, 19], [9, 15, 19]], 'ladder': False},
    '250251': {'node': [2, 5, 0], 'other_node': [2, 5, 1], 'open': False, 'blocks': [[8, 18, 4], [9, 18, 4]], 'ladder': False},
    '251252': {'node': [2, 5, 1], 'other_node': [2, 5, 2], 'open': False, 'blocks': [[8, 18, 7], [9, 18, 7]], 'ladder': False},
    '252253': {'node': [2, 5, 2], 'other_node': [2, 5, 3], 'open': False, 'blocks': [[8, 18, 10], [9, 18, 10]], 'ladder': False},
    '253254': {'node': [2, 5, 3], 'other_node': [2, 5, 4], 'open': False, 'blocks': [[8, 18, 13], [9, 18, 13]], 'ladder': False},
    '254255': {'node': [2, 5, 4], 'other_node': [2, 5, 5], 'open': False, 'blocks': [[8, 18, 16], [9, 18, 16]], 'ladder': False},
    '255256': {'node': [2, 5, 5], 'other_node': [2, 5, 6], 'open': False, 'blocks': [[8, 18, 19], [9, 18, 19]], 'ladder': False},
    '260261': {'node': [2, 6, 0], 'other_node': [2, 6, 1], 'open': False, 'blocks': [[8, 21, 4], [9, 21, 4]], 'ladder': False},
    '261262': {'node': [2, 6, 1], 'other_node': [2, 6, 2], 'open': False, 'blocks': [[8, 21, 7], [9, 21, 7]], 'ladder': False},
    '262263': {'node': [2, 6, 2], 'other_node': [2, 6, 3], 'open': False, 'blocks': [[8, 21, 10], [9, 21, 10]], 'ladder': False},
    '263264': {'node': [2, 6, 3], 'other_node': [2, 6, 4], 'open': False, 'blocks': [[8, 21, 13], [9, 21, 13]], 'ladder': False},
    '264265': {'node': [2, 6, 4], 'other_node': [2, 6, 5], 'open': False, 'blocks': [[8, 21, 16], [9, 21, 16]], 'ladder': False},
    '265266': {'node': [2, 6, 5], 'other_node': [2, 6, 6], 'open': False, 'blocks': [[8, 21, 19], [9, 21, 19]], 'ladder': False},

    # Floor 2 north-to-south edges
    '200210': {'node': [2, 0, 0], 'other_node': [2, 1, 0], 'open': False, 'blocks': [[8, 4, 2], [9, 4, 2]], 'ladder': False},
    '210220': {'node': [2, 1, 0], 'other_node': [2, 2, 0], 'open': False, 'blocks': [[8, 7, 2], [9, 7, 2]], 'ladder': False},
    '220230': {'node': [2, 2, 0], 'other_node': [2, 3, 0], 'open': False, 'blocks': [[8, 10, 2], [9, 10, 2]], 'ladder': False},
    '230240': {'node': [2, 3, 0], 'other_node': [2, 4, 0], 'open': False, 'blocks': [[8, 13, 2], [9, 13, 2]], 'ladder': False},
    '240250': {'node': [2, 4, 0], 'other_node': [2, 5, 0], 'open': False, 'blocks': [[8, 16, 2], [9, 16, 2]], 'ladder': False},
    '250260': {'node': [2, 5, 0], 'other_node': [2, 6, 0], 'open': False, 'blocks': [[8, 19, 2], [9, 19, 2]], 'ladder': False},
    '201211': {'node': [2, 0, 1], 'other_node': [2, 1, 1], 'open': False, 'blocks': [[8, 4, 5], [9, 4, 5]], 'ladder': False},
    '211221': {'node': [2, 1, 1], 'other_node': [2, 2, 1], 'open': False, 'blocks': [[8, 7, 5], [9, 7, 5]], 'ladder': False},
    '221231': {'node': [2, 2, 1], 'other_node': [2, 3, 1], 'open': False, 'blocks': [[8, 10, 5], [9, 10, 5]], 'ladder': False},
    '231241': {'node': [2, 3, 1], 'other_node': [2, 4, 1], 'open': False, 'blocks': [[8, 13, 5], [9, 13, 5]], 'ladder': False},
    '241251': {'node': [2, 4, 1], 'other_node': [2, 5, 1], 'open': False, 'blocks': [[8, 16, 5], [9, 16, 5]], 'ladder': False},
    '251261': {'node': [2, 5, 1], 'other_node': [2, 6, 1], 'open': False, 'blocks': [[8, 19, 5], [9, 19, 5]], 'ladder': False},
    '202212': {'node': [2, 0, 2], 'other_node': [2, 1, 2], 'open': False, 'blocks': [[8, 4, 8], [9, 4, 8]], 'ladder': False},
    '212222': {'node': [2, 1, 2], 'other_node': [2, 2, 2], 'open': False, 'blocks': [[8, 7, 8], [9, 7, 8]], 'ladder': False},
    '222232': {'node': [2, 2, 2], 'other_node': [2, 3, 2], 'open': False, 'blocks': [[8, 10, 8], [9, 10, 8]], 'ladder': False},
    '232242': {'node': [2, 3, 2], 'other_node': [2, 4, 2], 'open': False, 'blocks': [[8, 13, 8], [9, 13, 8]], 'ladder': False},
    '242252': {'node': [2, 4, 2], 'other_node': [2, 5, 2], 'open': False, 'blocks': [[8, 16, 8], [9, 16, 8]], 'ladder': False},
    '252262': {'node': [2, 5, 2], 'other_node': [2, 6, 2], 'open': False, 'blocks': [[8, 19, 8], [9, 19, 8]], 'ladder': False},
    '203213': {'node': [2, 0, 3], 'other_node': [2, 1, 3], 'open': False, 'blocks': [[8, 4, 11], [9, 4, 11]], 'ladder': False},
    '213223': {'node': [2, 1, 3], 'other_node': [2, 2, 3], 'open': False, 'blocks': [[8, 7, 11], [9, 7, 11]], 'ladder': False},
    '223233': {'node': [2, 2, 3], 'other_node': [2, 3, 3], 'open': False, 'blocks': [[8, 10, 11], [9, 10, 11]], 'ladder': False},
    '233243': {'node': [2, 3, 3], 'other_node': [2, 4, 3], 'open': False, 'blocks': [[8, 13, 11], [9, 13, 11]], 'ladder': False},
    '243253': {'node': [2, 4, 3], 'other_node': [2, 5, 3], 'open': False, 'blocks': [[8, 16, 11], [9, 16, 11]], 'ladder': False},
    '253263': {'node': [2, 5, 3], 'other_node': [2, 6, 3], 'open': False, 'blocks': [[8, 19, 11], [9, 19, 11]], 'ladder': False},
    '204214': {'node': [2, 0, 4], 'other_node': [2, 1, 4], 'open': False, 'blocks': [[8, 4, 14], [9, 4, 14]], 'ladder': False},
    '214224': {'node': [2, 1, 4], 'other_node': [2, 2, 4], 'open': False, 'blocks': [[8, 7, 14], [9, 7, 14]], 'ladder': False},
    '224234': {'node': [2, 2, 4], 'other_node': [2, 3, 4], 'open': False, 'blocks': [[8, 10, 14], [9, 10, 14]], 'ladder': False},
    '234244': {'node': [2, 3, 4], 'other_node': [2, 4, 4], 'open': False, 'blocks': [[8, 13, 14], [9, 13, 14]], 'ladder': False},
    '244254': {'node': [2, 4, 4], 'other_node': [2, 5, 4], 'open': False, 'blocks': [[8, 16, 14], [9, 16, 14]], 'ladder': False},
    '254264': {'node': [2, 5, 4], 'other_node': [2, 6, 4], 'open': False, 'blocks': [[8, 19, 14], [9, 19, 14]], 'ladder': False},
    '205215': {'node': [2, 0, 5], 'other_node': [2, 1, 5], 'open': False, 'blocks': [[8, 4, 17], [9, 4, 17]], 'ladder': False},
    '215225': {'node': [2, 1, 5], 'other_node': [2, 2, 5], 'open': False, 'blocks': [[8, 7, 17], [9, 7, 17]], 'ladder': False},
    '225235': {'node': [2, 2, 5], 'other_node': [2, 3, 5], 'open': False, 'blocks': [[8, 10, 17], [9, 10, 17]], 'ladder': False},
    '235245': {'node': [2, 3, 5], 'other_node': [2, 4, 5], 'open': False, 'blocks': [[8, 13, 17], [9, 13, 17]], 'ladder': False},
    '245255': {'node': [2, 4, 5], 'other_node': [2, 5, 5], 'open': False, 'blocks': [[8, 16, 17], [9, 16, 17]], 'ladder': False},
    '255265': {'node': [2, 5, 5], 'other_node': [2, 6, 5], 'open': False, 'blocks': [[8, 19, 17], [9, 19, 17]], 'ladder': False},
    '206216': {'node': [2, 0, 6], 'other_node': [2, 1, 6], 'open': False, 'blocks': [[8, 4, 20], [9, 4, 20]], 'ladder': False},
    '216226': {'node': [2, 1, 6], 'other_node': [2, 2, 6], 'open': False, 'blocks': [[8, 7, 20], [9, 7, 20]], 'ladder': False},
    '226236': {'node': [2, 2, 6], 'other_node': [2, 3, 6], 'open': False, 'blocks': [[8, 10, 20], [9, 10, 20]], 'ladder': False},
    '236246': {'node': [2, 3, 6], 'other_node': [2, 4, 6], 'open': False, 'blocks': [[8, 13, 20], [9, 13, 20]], 'ladder': False},
    '246256': {'node': [2, 4, 6], 'other_node': [2, 5, 6], 'open': False, 'blocks': [[8, 16, 20], [9, 16, 20]], 'ladder': False},
    '256266': {'node': [2, 5, 6], 'other_node': [2, 6, 6], 'open': False, 'blocks': [[8, 19, 20], [9, 19, 20]], 'ladder': False},

    # Floor 3 bottom-to-top edges
    '200300': {'node': [2, 0, 0], 'other_node': [3, 0, 0], 'open': False, 'blocks': [[10, 2, 3]], 'ladder': True},
    '201301': {'node': [2, 0, 1], 'other_node': [3, 0, 1], 'open': False, 'blocks': [[10, 2, 6]], 'ladder': True},
    '202302': {'node': [2, 0, 2], 'other_node': [3, 0, 2], 'open': False, 'blocks': [[10, 2, 9]], 'ladder': True},
    '203303': {'node': [2, 0, 3], 'other_node': [3, 0, 3], 'open': False, 'blocks': [[10, 2, 12]], 'ladder': True},
    '204304': {'node': [2, 0, 4], 'other_node': [3, 0, 4], 'open': False, 'blocks': [[10, 2, 15]], 'ladder': True},
    '205305': {'node': [2, 0, 5], 'other_node': [3, 0, 5], 'open': False, 'blocks': [[10, 2, 18]], 'ladder': True},
    '206306': {'node': [2, 0, 6], 'other_node': [3, 0, 6], 'open': False, 'blocks': [[10, 2, 21]], 'ladder': True},
    '210310': {'node': [2, 1, 0], 'other_node': [3, 1, 0], 'open': False, 'blocks': [[10, 5, 3]], 'ladder': True},
    '211311': {'node': [2, 1, 1], 'other_node': [3, 1, 1], 'open': False, 'blocks': [[10, 5, 6]], 'ladder': True},
    '212312': {'node': [2, 1, 2], 'other_node': [3, 1, 2], 'open': False, 'blocks': [[10, 5, 9]], 'ladder': True},
    '213313': {'node': [2, 1, 3], 'other_node': [3, 1, 3], 'open': False, 'blocks': [[10, 5, 12]], 'ladder': True},
    '214314': {'node': [2, 1, 4], 'other_node': [3, 1, 4], 'open': False, 'blocks': [[10, 5, 15]], 'ladder': True},
    '215315': {'node': [2, 1, 5], 'other_node': [3, 1, 5], 'open': False, 'blocks': [[10, 5, 18]], 'ladder': True},
    '216316': {'node': [2, 1, 6], 'other_node': [3, 1, 6], 'open': False, 'blocks': [[10, 5, 21]], 'ladder': True},
    '220320': {'node': [2, 2, 0], 'other_node': [3, 2, 0], 'open': False, 'blocks': [[10, 8, 3]], 'ladder': True},
    '221321': {'node': [2, 2, 1], 'other_node': [3, 2, 1], 'open': False, 'blocks': [[10, 8, 6]], 'ladder': True},
    '222322': {'node': [2, 2, 2], 'other_node': [3, 2, 2], 'open': False, 'blocks': [[10, 8, 9]], 'ladder': True},
    '223323': {'node': [2, 2, 3], 'other_node': [3, 2, 3], 'open': False, 'blocks': [[10, 8, 12]], 'ladder': True},
    '224324': {'node': [2, 2, 4], 'other_node': [3, 2, 4], 'open': False, 'blocks': [[10, 8, 15]], 'ladder': True},
    '225325': {'node': [2, 2, 5], 'other_node': [3, 2, 5], 'open': False, 'blocks': [[10, 8, 18]], 'ladder': True},
    '226326': {'node': [2, 2, 6], 'other_node': [3, 2, 6], 'open': False, 'blocks': [[10, 8, 21]], 'ladder': True},
    '230330': {'node': [2, 3, 0], 'other_node': [3, 3, 0], 'open': False, 'blocks': [[10, 11, 3]], 'ladder': True},
    '231331': {'node': [2, 3, 1], 'other_node': [3, 3, 1], 'open': False, 'blocks': [[10, 11, 6]], 'ladder': True},
    '232332': {'node': [2, 3, 2], 'other_node': [3, 3, 2], 'open': False, 'blocks': [[10, 11, 9]], 'ladder': True},
    '233333': {'node': [2, 3, 3], 'other_node': [3, 3, 3], 'open': False, 'blocks': [[10, 11, 12]], 'ladder': True},
    '234334': {'node': [2, 3, 4], 'other_node': [3, 3, 4], 'open': False, 'blocks': [[10, 11, 15]], 'ladder': True},
    '235335': {'node': [2, 3, 5], 'other_node': [3, 3, 5], 'open': False, 'blocks': [[10, 11, 18]], 'ladder': True},
    '236336': {'node': [2, 3, 6], 'other_node': [3, 3, 6], 'open': False, 'blocks': [[10, 11, 21]], 'ladder': True},
    '240340': {'node': [2, 4, 0], 'other_node': [3, 4, 0], 'open': False, 'blocks': [[10, 14, 3]], 'ladder': True},
    '241341': {'node': [2, 4, 1], 'other_node': [3, 4, 1], 'open': False, 'blocks': [[10, 14, 6]], 'ladder': True},
    '242342': {'node': [2, 4, 2], 'other_node': [3, 4, 2], 'open': False, 'blocks': [[10, 14, 9]], 'ladder': True},
    '243343': {'node': [2, 4, 3], 'other_node': [3, 4, 3], 'open': False, 'blocks': [[10, 14, 12]], 'ladder': True},
    '244344': {'node': [2, 4, 4], 'other_node': [3, 4, 4], 'open': False, 'blocks': [[10, 14, 15]], 'ladder': True},
    '245345': {'node': [2, 4, 5], 'other_node': [3, 4, 5], 'open': False, 'blocks': [[10, 14, 18]], 'ladder': True},
    '246346': {'node': [2, 4, 6], 'other_node': [3, 4, 6], 'open': False, 'blocks': [[10, 14, 21]], 'ladder': True},
    '250350': {'node': [2, 5, 0], 'other_node': [3, 5, 0], 'open': False, 'blocks': [[10, 17, 3]], 'ladder': True},
    '251351': {'node': [2, 5, 1], 'other_node': [3, 5, 1], 'open': False, 'blocks': [[10, 17, 6]], 'ladder': True},
    '252352': {'node': [2, 5, 2], 'other_node': [3, 5, 2], 'open': False, 'blocks': [[10, 17, 9]], 'ladder': True},
    '253353': {'node': [2, 5, 3], 'other_node': [3, 5, 3], 'open': False, 'blocks': [[10, 17, 12]], 'ladder': True},
    '254354': {'node': [2, 5, 4], 'other_node': [3, 5, 4], 'open': False, 'blocks': [[10, 17, 15]], 'ladder': True},
    '255355': {'node': [2, 5, 5], 'other_node': [3, 5, 5], 'open': False, 'blocks': [[10, 17, 18]], 'ladder': True},
    '256356': {'node': [2, 5, 6], 'other_node': [3, 5, 6], 'open': False, 'blocks': [[10, 17, 21]], 'ladder': True},
    '260360': {'node': [2, 6, 0], 'other_node': [3, 6, 0], 'open': False, 'blocks': [[10, 20, 3]], 'ladder': True},
    '261361': {'node': [2, 6, 1], 'other_node': [3, 6, 1], 'open': False, 'blocks': [[10, 20, 6]], 'ladder': True},
    '262362': {'node': [2, 6, 2], 'other_node': [3, 6, 2], 'open': False, 'blocks': [[10, 20, 9]], 'ladder': True},
    '263363': {'node': [2, 6, 3], 'other_node': [3, 6, 3], 'open': False, 'blocks': [[10, 20, 12]], 'ladder': True},
    '264364': {'node': [2, 6, 4], 'other_node': [3, 6, 4], 'open': False, 'blocks': [[10, 20, 15]], 'ladder': True},
    '265365': {'node': [2, 6, 5], 'other_node': [3, 6, 5], 'open': False, 'blocks': [[10, 20, 18]], 'ladder': True},
    '266366': {'node': [2, 6, 6], 'other_node': [3, 6, 6], 'open': False, 'blocks': [[10, 20, 21]], 'ladder': True},
    
    # Floor 3 west-to-east edges
    '300301': {'node': [3, 0, 0], 'other_node': [3, 0, 1], 'open': False, 'blocks': [[11, 3, 4], [12, 3, 4]], 'ladder': False},
    '301302': {'node': [3, 0, 1], 'other_node': [3, 0, 2], 'open': False, 'blocks': [[11, 3, 7], [12, 3, 7]], 'ladder': False},
    '302303': {'node': [3, 0, 2], 'other_node': [3, 0, 3], 'open': False, 'blocks': [[11, 3, 10], [12, 3, 10]], 'ladder': False},
    '303304': {'node': [3, 0, 3], 'other_node': [3, 0, 4], 'open': False, 'blocks': [[11, 3, 13], [12, 3, 13]], 'ladder': False},
    '304305': {'node': [3, 0, 4], 'other_node': [3, 0, 5], 'open': False, 'blocks': [[11, 3, 16], [12, 3, 16]], 'ladder': False},
    '305306': {'node': [3, 0, 5], 'other_node': [3, 0, 6], 'open': False, 'blocks': [[11, 3, 19], [12, 3, 19]], 'ladder': False},
    '310311': {'node': [3, 1, 0], 'other_node': [3, 1, 1], 'open': False, 'blocks': [[11, 6, 4], [12, 6, 4]], 'ladder': False},
    '311312': {'node': [3, 1, 1], 'other_node': [3, 1, 2], 'open': False, 'blocks': [[11, 6, 7], [12, 6, 7]], 'ladder': False},
    '312313': {'node': [3, 1, 2], 'other_node': [3, 1, 3], 'open': False, 'blocks': [[11, 6, 10], [12, 6, 10]], 'ladder': False},
    '313314': {'node': [3, 1, 3], 'other_node': [3, 1, 4], 'open': False, 'blocks': [[11, 6, 13], [12, 6, 13]], 'ladder': False},
    '314315': {'node': [3, 1, 4], 'other_node': [3, 1, 5], 'open': False, 'blocks': [[11, 6, 16], [12, 6, 16]], 'ladder': False},
    '315316': {'node': [3, 1, 5], 'other_node': [3, 1, 6], 'open': False, 'blocks': [[11, 6, 19], [12, 6, 19]], 'ladder': False},
    '320321': {'node': [3, 2, 0], 'other_node': [3, 2, 1], 'open': False, 'blocks': [[11, 9, 4], [12, 9, 4]], 'ladder': False},
    '321322': {'node': [3, 2, 1], 'other_node': [3, 2, 2], 'open': False, 'blocks': [[11, 9, 7], [12, 9, 7]], 'ladder': False},
    '322323': {'node': [3, 2, 2], 'other_node': [3, 2, 3], 'open': False, 'blocks': [[11, 9, 10], [12, 9, 10]], 'ladder': False},
    '323324': {'node': [3, 2, 3], 'other_node': [3, 2, 4], 'open': False, 'blocks': [[11, 9, 13], [12, 9, 13]], 'ladder': False},
    '324325': {'node': [3, 2, 4], 'other_node': [3, 2, 5], 'open': False, 'blocks': [[11, 9, 16], [12, 9, 16]], 'ladder': False},
    '325326': {'node': [3, 2, 5], 'other_node': [3, 2, 6], 'open': False, 'blocks': [[11, 9, 19], [12, 9, 19]], 'ladder': False},
    '330331': {'node': [3, 3, 0], 'other_node': [3, 3, 1], 'open': False, 'blocks': [[11, 12, 4], [12, 12, 4]], 'ladder': False},
    '331332': {'node': [3, 3, 1], 'other_node': [3, 3, 2], 'open': False, 'blocks': [[11, 12, 7], [12, 12, 7]], 'ladder': False},
    '332333': {'node': [3, 3, 2], 'other_node': [3, 3, 3], 'open': False, 'blocks': [[11, 12, 10], [12, 12, 10]], 'ladder': False},
    '333334': {'node': [3, 3, 3], 'other_node': [3, 3, 4], 'open': False, 'blocks': [[11, 12, 13], [12, 12, 13]], 'ladder': False},
    '334335': {'node': [3, 3, 4], 'other_node': [3, 3, 5], 'open': False, 'blocks': [[11, 12, 16], [12, 12, 16]], 'ladder': False},
    '335336': {'node': [3, 3, 5], 'other_node': [3, 3, 6], 'open': False, 'blocks': [[11, 12, 19], [12, 12, 19]], 'ladder': False},
    '340341': {'node': [3, 4, 0], 'other_node': [3, 4, 1], 'open': False, 'blocks': [[11, 15, 4], [12, 15, 4]], 'ladder': False},
    '341342': {'node': [3, 4, 1], 'other_node': [3, 4, 2], 'open': False, 'blocks': [[11, 15, 7], [12, 15, 7]], 'ladder': False},
    '342343': {'node': [3, 4, 2], 'other_node': [3, 4, 3], 'open': False, 'blocks': [[11, 15, 10], [12, 15, 10]], 'ladder': False},
    '343344': {'node': [3, 4, 3], 'other_node': [3, 4, 4], 'open': False, 'blocks': [[11, 15, 13], [12, 15, 13]], 'ladder': False},
    '344345': {'node': [3, 4, 4], 'other_node': [3, 4, 5], 'open': False, 'blocks': [[11, 15, 16], [12, 15, 16]], 'ladder': False},
    '345346': {'node': [3, 4, 5], 'other_node': [3, 4, 6], 'open': False, 'blocks': [[11, 15, 19], [12, 15, 19]], 'ladder': False},
    '350351': {'node': [3, 5, 0], 'other_node': [3, 5, 1], 'open': False, 'blocks': [[11, 18, 4], [12, 18, 4]], 'ladder': False},
    '351352': {'node': [3, 5, 1], 'other_node': [3, 5, 2], 'open': False, 'blocks': [[11, 18, 7], [12, 18, 7]], 'ladder': False},
    '352353': {'node': [3, 5, 2], 'other_node': [3, 5, 3], 'open': False, 'blocks': [[11, 18, 10], [12, 18, 10]], 'ladder': False},
    '353354': {'node': [3, 5, 3], 'other_node': [3, 5, 4], 'open': False, 'blocks': [[11, 18, 13], [12, 18, 13]], 'ladder': False},
    '354355': {'node': [3, 5, 4], 'other_node': [3, 5, 5], 'open': False, 'blocks': [[11, 18, 16], [12, 18, 16]], 'ladder': False},
    '355356': {'node': [3, 5, 5], 'other_node': [3, 5, 6], 'open': False, 'blocks': [[11, 18, 19], [12, 18, 19]], 'ladder': False},
    '360361': {'node': [3, 6, 0], 'other_node': [3, 6, 1], 'open': False, 'blocks': [[11, 21, 4], [12, 21, 4]], 'ladder': False},
    '361362': {'node': [3, 6, 1], 'other_node': [3, 6, 2], 'open': False, 'blocks': [[11, 21, 7], [12, 21, 7]], 'ladder': False},
    '362363': {'node': [3, 6, 2], 'other_node': [3, 6, 3], 'open': False, 'blocks': [[11, 21, 10], [12, 21, 10]], 'ladder': False},
    '363364': {'node': [3, 6, 3], 'other_node': [3, 6, 4], 'open': False, 'blocks': [[11, 21, 13], [12, 21, 13]], 'ladder': False},
    '364365': {'node': [3, 6, 4], 'other_node': [3, 6, 5], 'open': False, 'blocks': [[11, 21, 16], [12, 21, 16]], 'ladder': False},
    '365366': {'node': [3, 6, 5], 'other_node': [3, 6, 6], 'open': False, 'blocks': [[11, 21, 19], [12, 21, 19]], 'ladder': False},

    # Floor 3 north-to-south edges
    '300310': {'node': [3, 0, 0], 'other_node': [3, 1, 0], 'open': False, 'blocks': [[11, 4, 2], [12, 4, 2]], 'ladder': False},
    '310320': {'node': [3, 1, 0], 'other_node': [3, 2, 0], 'open': False, 'blocks': [[11, 7, 2], [12, 7, 2]], 'ladder': False},
    '320330': {'node': [3, 2, 0], 'other_node': [3, 3, 0], 'open': False, 'blocks': [[11, 10, 2], [12, 10, 2]], 'ladder': False},
    '330340': {'node': [3, 3, 0], 'other_node': [3, 4, 0], 'open': False, 'blocks': [[11, 13, 2], [12, 13, 2]], 'ladder': False},
    '340350': {'node': [3, 4, 0], 'other_node': [3, 5, 0], 'open': False, 'blocks': [[11, 16, 2], [12, 16, 2]], 'ladder': False},
    '350360': {'node': [3, 5, 0], 'other_node': [3, 6, 0], 'open': False, 'blocks': [[11, 19, 2], [12, 19, 2]], 'ladder': False},
    '301311': {'node': [3, 0, 1], 'other_node': [3, 1, 1], 'open': False, 'blocks': [[11, 4, 5], [12, 4, 5]], 'ladder': False},
    '311321': {'node': [3, 1, 1], 'other_node': [3, 2, 1], 'open': False, 'blocks': [[11, 7, 5], [12, 7, 5]], 'ladder': False},
    '321331': {'node': [3, 2, 1], 'other_node': [3, 3, 1], 'open': False, 'blocks': [[11, 10, 5], [12, 10, 5]], 'ladder': False},
    '331341': {'node': [3, 3, 1], 'other_node': [3, 4, 1], 'open': False, 'blocks': [[11, 13, 5], [12, 13, 5]], 'ladder': False},
    '341351': {'node': [3, 4, 1], 'other_node': [3, 5, 1], 'open': False, 'blocks': [[11, 16, 5], [12, 16, 5]], 'ladder': False},
    '351361': {'node': [3, 5, 1], 'other_node': [3, 6, 1], 'open': False, 'blocks': [[11, 19, 5], [12, 19, 5]], 'ladder': False},
    '302312': {'node': [3, 0, 2], 'other_node': [3, 1, 2], 'open': False, 'blocks': [[11, 4, 8], [12, 4, 8]], 'ladder': False},
    '312322': {'node': [3, 1, 2], 'other_node': [3, 2, 2], 'open': False, 'blocks': [[11, 7, 8], [12, 7, 8]], 'ladder': False},
    '322332': {'node': [3, 2, 2], 'other_node': [3, 3, 2], 'open': False, 'blocks': [[11, 10, 8], [12, 10, 8]], 'ladder': False},
    '332342': {'node': [3, 3, 2], 'other_node': [3, 4, 2], 'open': False, 'blocks': [[11, 13, 8], [12, 13, 8]], 'ladder': False},
    '342352': {'node': [3, 4, 2], 'other_node': [3, 5, 2], 'open': False, 'blocks': [[11, 16, 8], [12, 16, 8]], 'ladder': False},
    '352362': {'node': [3, 5, 2], 'other_node': [3, 6, 2], 'open': False, 'blocks': [[11, 19, 8], [12, 19, 8]], 'ladder': False},
    '303313': {'node': [3, 0, 3], 'other_node': [3, 1, 3], 'open': False, 'blocks': [[11, 4, 11], [12, 4, 11]], 'ladder': False},
    '313323': {'node': [3, 1, 3], 'other_node': [3, 2, 3], 'open': False, 'blocks': [[11, 7, 11], [12, 7, 11]], 'ladder': False},
    '323333': {'node': [3, 2, 3], 'other_node': [3, 3, 3], 'open': False, 'blocks': [[11, 10, 11], [12, 10, 11]], 'ladder': False},
    '333343': {'node': [3, 3, 3], 'other_node': [3, 4, 3], 'open': False, 'blocks': [[11, 13, 11], [12, 13, 11]], 'ladder': False},
    '343353': {'node': [3, 4, 3], 'other_node': [3, 5, 3], 'open': False, 'blocks': [[11, 16, 11], [12, 16, 11]], 'ladder': False},
    '353363': {'node': [3, 5, 3], 'other_node': [3, 6, 3], 'open': False, 'blocks': [[11, 19, 11], [12, 19, 11]], 'ladder': False},
    '304314': {'node': [3, 0, 4], 'other_node': [3, 1, 4], 'open': False, 'blocks': [[11, 4, 14], [12, 4, 14]], 'ladder': False},
    '314324': {'node': [3, 1, 4], 'other_node': [3, 2, 4], 'open': False, 'blocks': [[11, 7, 14], [12, 7, 14]], 'ladder': False},
    '324334': {'node': [3, 2, 4], 'other_node': [3, 3, 4], 'open': False, 'blocks': [[11, 10, 14], [12, 10, 14]], 'ladder': False},
    '334344': {'node': [3, 3, 4], 'other_node': [3, 4, 4], 'open': False, 'blocks': [[11, 13, 14], [12, 13, 14]], 'ladder': False},
    '344354': {'node': [3, 4, 4], 'other_node': [3, 5, 4], 'open': False, 'blocks': [[11, 16, 14], [12, 16, 14]], 'ladder': False},
    '354364': {'node': [3, 5, 4], 'other_node': [3, 6, 4], 'open': False, 'blocks': [[11, 19, 14], [12, 19, 14]], 'ladder': False},
    '305315': {'node': [3, 0, 5], 'other_node': [3, 1, 5], 'open': False, 'blocks': [[11, 4, 17], [12, 4, 17]], 'ladder': False},
    '315325': {'node': [3, 1, 5], 'other_node': [3, 2, 5], 'open': False, 'blocks': [[11, 7, 17], [12, 7, 17]], 'ladder': False},
    '325335': {'node': [3, 2, 5], 'other_node': [3, 3, 5], 'open': False, 'blocks': [[11, 10, 17], [12, 10, 17]], 'ladder': False},
    '335345': {'node': [3, 3, 5], 'other_node': [3, 4, 5], 'open': False, 'blocks': [[11, 13, 17], [12, 13, 17]], 'ladder': False},
    '345355': {'node': [3, 4, 5], 'other_node': [3, 5, 5], 'open': False, 'blocks': [[11, 16, 17], [12, 16, 17]], 'ladder': False},
    '355365': {'node': [3, 5, 5], 'other_node': [3, 6, 5], 'open': False, 'blocks': [[11, 19, 17], [12, 19, 17]], 'ladder': False},
    '306316': {'node': [3, 0, 6], 'other_node': [3, 1, 6], 'open': False, 'blocks': [[11, 4, 20], [12, 4, 20]], 'ladder': False},
    '316326': {'node': [3, 1, 6], 'other_node': [3, 2, 6], 'open': False, 'blocks': [[11, 7, 20], [12, 7, 20]], 'ladder': False},
    '326336': {'node': [3, 2, 6], 'other_node': [3, 3, 6], 'open': False, 'blocks': [[11, 10, 20], [12, 10, 20]], 'ladder': False},
    '336346': {'node': [3, 3, 6], 'other_node': [3, 4, 6], 'open': False, 'blocks': [[11, 13, 20], [12, 13, 20]], 'ladder': False},
    '346356': {'node': [3, 4, 6], 'other_node': [3, 5, 6], 'open': False, 'blocks': [[11, 16, 20], [12, 16, 20]], 'ladder': False},
    '356366': {'node': [3, 5, 6], 'other_node': [3, 6, 6], 'open': False, 'blocks': [[11, 19, 20], [12, 19, 20]], 'ladder': False},
}

included = set({})
excluded = set({})
directions = {}

def tostr(coords):
    [layer, row, column] = coords
    return '{}{}{}'.format(layer, row, column)

def tolist(coords_str):
    coords = [
        int(coords_str[0]),
        int(coords_str[1]),
        int(coords_str[2]),
    ]
    return coords


# Referencing a node (aka chamber) looks like this:
# nodes[height][row][column]
# where row starts at 0 and goes from west to
# east, column starts at 0 and goes from north
# to south, and height starts at 0 and goes
# from bottom to top. Each node is a dictionary
# of its attributes, including the indices of the
# neighboring nodes and whether it has been visited
num_node_rows = 7
num_node_columns = 7
num_node_layers = 4
nodes = []
for layer in range(num_node_layers):
    nodes.append([])
    for row in range(num_node_rows):
        nodes[layer].append([])
        for column in range(num_node_columns):
            index = [layer, row, column]
            nodes[layer][row].append({
                'index': index,
                'neighbors': [],
                'included': False,
            })
            excluded.add(tostr(index))
for key in edges:
    edge = edges[key]
    [layer, row, column] = edge['node']
    [other_layer, other_row, other_column] = edge['other_node']
    nodes[layer][row][column]['neighbors'].append([other_layer, other_row, other_column])
    nodes[other_layer][other_row][other_column]['neighbors'].append([layer, row, column])

### STEPS ###
'''
1. add start node to maze (mark on node itself, add to included set, remove from excluded set)
2. repeat while excluded set is non-empty:
   1. do a random walk to discover potentials
      1. choose a new random node not in the maze, called potential_start
      2. set a new set called potentials to be an empty set
      3. add potential_start to potentials (add as string)
      4. set current to potential_start
      5. repeat while current is not in maze:
         1. randomly walk (update current to a random neighbor)
         2. add current to potentials
         3. record the neighbor walked to in directions dict only if not recorded for that node yet
   2. do a real walk following recorded directions
      1. set current to potential_start
      2. repeat while current is not in maze:
         1. remove current node from potentials
         2. add current node to maze
         3. walk to the neighbor denoted by directions dict (update current to be neighbor)
         4. mark the traversed edge as open
         5. mark the traversed edge's blocks with the new letter for being open
'''

def add_to_maze(node):
    [layer, row, column] = node
    nodes[layer][row][column]['included'] = True
    node_string = tostr(node)
    included.add(node_string)
    excluded.discard(node_string)

def walk(node):
    [layer, row, column] = node
    neighbors = [tostr(n) for n in nodes[layer][row][column]['neighbors']]
    new_node_string = random.choice(neighbors)
    # Record the direction we went if not recorded yet
    directions[tostr(node)] = directions.get(tostr(node), new_node_string)
    return tolist(new_node_string)

def walk_direction(node):
    new_node_string = directions[tostr(node)]
    return tolist(new_node_string)

def mark_edge_as_open(node1, node2):
    key1 = ''.join([tostr(node1), tostr(node2)])
    key2 = ''.join([tostr(node2), tostr(node1)])
    edge = edges[key1] if key1 in edges else edges[key2]
    edge['open'] = True
    for block in edge['blocks']:
        [l, r, c] = block
        blocks[l][r][c] = 'L' if edge['ladder'] else 'O'

def get_south_edge_blocks(node):
    [layer, row, column] = node
    block1_layer = (layer + 1) * 3 - 1
    block1_row = (row + 1) * 3 + 1
    block1_column = (column + 1) * 3 - 1
    block2_layer = (layer + 1) * 3
    block2_row = (row + 1) * 3 + 1
    block2_column = (column + 1) * 3 - 1
    block1 = [block1_layer, block1_row, block1_column]
    block2 = [block2_layer, block2_row, block2_column]
    return [block1, block2]

def get_start_platform_blocks(node):
    [layer, row, column] = node
    block1_layer = (layer + 1) * 3 - 2
    block1_row = (row + 1) * 3 + 2
    block1_column = (column + 1) * 3 - 1
    block2_layer = (layer + 1) * 3 - 2
    block2_row = (row + 1) * 3 + 2
    block2_column = (column + 1) * 3
    block1 = [block1_layer, block1_row, block1_column]
    block2 = [block2_layer, block2_row, block2_column]
    return [block1, block2]

def get_start_signpost_block(node):
    [layer, row, column] = node
    block_layer = (layer + 1) * 3 - 1
    block_row = (row + 1) * 3 + 2
    block_column = (column + 1) * 3
    block = [block_layer, block_row, block_column]
    return block

def get_finish_ladder_blocks(node):
    [layer, row, column] = node
    block1_layer = (layer + 1) * 3 + 1
    block1_row = (row + 1) * 3 - 1
    block1_column = (column + 1) * 3
    block2_layer = (layer + 1) * 3 + 2
    block2_row = (row + 1) * 3 - 1
    block2_column = (column + 1) * 3
    block3_layer = (layer + 1) * 3 + 3
    block3_row = (row + 1) * 3 - 1
    block3_column = (column + 1) * 3
    block1 = [block1_layer, block1_row, block1_column]
    block2 = [block2_layer, block2_row, block2_column]
    block3 = [block3_layer, block3_row, block3_column]
    return [block1, block2, block3]

def get_finish_solid_blocks(node):
    [layer, row, column] = node
    block1_layer = (layer + 1) * 3 + 2
    block1_row = (row + 1) * 3 - 2
    block1_column = (column + 1) * 3
    block2_layer = (layer + 1) * 3 + 3
    block2_row = (row + 1) * 3 - 2
    block2_column = (column + 1) * 3
    block1 = [block1_layer, block1_row, block1_column]
    block2 = [block2_layer, block2_row, block2_column]
    return [block1, block2]

def get_finish_signpost_block(node):
    [layer, row, column] = node
    block_layer = (layer + 1) * 3 + 2
    block_row = (row + 1) * 3 - 2
    block_column = (column + 1) * 3 + 1
    block = [block_layer, block_row, block_column]
    return block

def print_results():
    counts = {
        'B': 0,
        'S': 0,
        '1': 0,
        '2': 0,
        'L': 0,
        'D': 0,
        'O': 0,
    }
    for layer in blocks:
        for row in layer:
            for block in row:
                counts[block] += 1
    print({'counts': counts})
    print()
    for layer in blocks:
        for row in layer:
            print(' '.join(row))
        print()

def main():
    # Randomly pick a start node.
    start_layer = 0
    start_row = num_node_rows - 1
    start_column = random.choice(range(num_node_columns))
    start_node = [start_layer, start_row, start_column]

    # Randomly pick a finish node.
    finish_layer = num_node_layers - 1
    finish_row = random.choice(range(num_node_rows // 2)) # Somewhere in the north half
    finish_column = random.choice(range(num_node_columns))
    finish_node = [finish_layer, finish_row, finish_column]

    add_to_maze([start_layer, start_row, start_column])

    # Wilson's algorithm
    while len(excluded) > 0:
        # do a random walk to discover potentials
        potential_start_string = random.choice(list(excluded))
        potential_start = tolist(potential_start_string)
        potentials = set({})
        potentials.add(potential_start_string)
        current = potential_start
        while tostr(current) in excluded:
            current = walk(current)
            potentials.add(tostr(current))

        # do a real walk based on recorded directions
        current = potential_start
        while tostr(current) in excluded:
            potentials.discard(tostr(current))
            add_to_maze(current)
            prev = current
            current = walk_direction(current)
            mark_edge_as_open(prev, current)
        directions.clear()

    # Create maze entrance
    for block in get_south_edge_blocks(start_node):
        [l, r, c] = block
        blocks[l][r][c] = 'D'
    for block in get_start_platform_blocks(start_node):
        [l, r, c] = block
        blocks[l][r][c] = 'B'
    [l, r, c] = get_start_signpost_block(start_node)
    blocks[l][r][c] = '1'

    # Create maze exit
    for block in get_finish_ladder_blocks(finish_node):
        [l, r, c] = block
        blocks[l][r][c] = 'L'
    for block in get_finish_solid_blocks(finish_node):
        [l, r, c] = block
        blocks[l][r][c] = 'B'
    [l, r, c] = get_finish_signpost_block(finish_node)
    blocks[l][r][c] = '2'
    
    print_results()

main()
