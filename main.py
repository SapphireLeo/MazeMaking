# main.py

import Maze

maze = Maze.Maze(40, 40)

maze.make_stem(0, 1, [])

maze.search(0, 1)

maze.print_maze()