# Maze.py

import os
import copy
import random

# unicode and string set of special characters, representing the maze.
SQUARE_UNICODE = 9608
SQUARE = chr(SQUARE_UNICODE) * 2
RHOMBUS_UNICODE = 9670
RHOMBUS = chr(RHOMBUS_UNICODE) + ' '
ARROW_DOWN_UNICODE = 9660
ARROW_DOWN = chr(ARROW_DOWN_UNICODE) + ' '

# set of direction. In order, it is (down, right, up, left).
direction = ((1, 0), (0, 1), (-1, 0), (0, -1))


# printing function in various colors.
def color_print(string, color):
    # print in bright white color. (wall of maze)
    if color == 'BrightWhite':
        print('\x1b[97m' + string + '\x1b[0m', end='')
    # print in bright yellow color. (border of maze)
    if color == 'BrightYellow':
        print('\x1b[93m' + string + '\x1b[0m', end='')
    # print in bright blue color. (solution path)
    if color == 'BrightBlue':
        print('\x1b[94m' + string + '\x1b[0m', end='')


# defining Maze class.
class Maze:
    def __init__(self, col_size, row_size):
        # initialize maze as 2-dimension array.
        self.maze = [[1 for col in range(col_size)] for row in range(row_size)]

        # store the size of maze. (row, column)
        self.row_num = row_size
        self.col_num = col_size

        # create the visited node set, and solution path node set. the size of them is copy of original maze.
        self.visited = [[False for col in range(col_size)] for row in range(row_size)]
        self.solution = [[False for col in range(col_size)] for row in range(row_size)]

        # mark the border of the maze as integer 2.
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if y == 0 or y == len(self.maze) - 1 or x == 0 or x == len(self.maze[y]) - 1:
                    self.maze[y][x] = 2

        # create the entrance and exit of the maze. mark them as integer 1 in maze and string in solution set.
        self.maze[0][1] = self.maze[-1][-2] = 1
        self.solution[0][1] = 'in'
        self.solution[-1][-2] = 'out'

        # set the minimum and maximum solution size. it differs as the total size of maze changes.
        self.min_solution_size = (col_size ** 2 + row_size ** 2) ** 0.5 * 2
        self.max_solution_size = (col_size ** 2 + row_size ** 2) ** 0.5 * 2.5

        # set the minium and maximum depth of branch path(not solution path).
        self.min_depth = 4
        self.max_depth = 8

    # printing method of maze.
    def print_maze(self):
        # store the string value and printing color in "buffer" tuple, and print it at once.
        for y, row in enumerate(self.maze):
            for x, grid in enumerate(row):
                # if the grid is empty(path)
                if grid == 0:
                    # if the grid is the entrance or exit, print an ARROW mark.
                    if self.solution[y][x] == 'in' or self.solution[y][x] == 'out':
                        buffer = ARROW_DOWN + ' ', 'BrightBlue'
                    # if the grid is the part of solution path, print an RHOMBUS mark.
                    elif self.solution[y][x]:
                        buffer = RHOMBUS + ' ', 'BrightBlue'
                    # if the grid is just empty(path), print it as an empty space.
                    else:
                        buffer = ' ' * 3, 'BrightWhite'
                # if the grid is the border of maze, print it in yellow square.
                elif grid == 2:
                    buffer = SQUARE + ' ', 'BrightYellow'
                # if the grid is the just wall, print it in white square.
                else:
                    buffer = SQUARE + ' ', 'BrightWhite'
                # use color_print method with parameters buffer.
                color_print(buffer[0], buffer[1])
            # change the line.
            print()

    # it is not used.
    def clear_print(self):
        os.system('cls')  # not working on Pycharm IDE
        self.print_maze()

    # set the maze into given maze array(2-dimension).
    def set_maze(self, new_maze):
        # if it is not valid form of maze, return False.
        for y, row in enumerate(new_maze):
            for x, grid in enumerate(row):
                if y == 0 or y == len(new_maze) - 1 or x == 0 or x == len(row) - 1:
                    if y == 0 and x == 1:
                        # the entrance of maze must exist.
                        if grid != 0:
                            return False
                    elif y == len(new_maze) - 1 and x == len(row) - 2:
                        # the exit of maze must exist.
                        if grid != 0:
                            return False
                    else:
                        # the border of maze must be wall.
                        if grid != 2:
                            return False
        # set the maze.
        self.maze = copy.deepcopy(new_maze)
        self.visited = copy.deepcopy(new_maze)
        self.solution = copy.deepcopy(new_maze)

        # initialize all node to unvisited and not solution.
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.visited[y][x] != 2:
                    self.visited[y][x] = False
                self.solution[y][x] = False
        # initialize the entrance and exit of maze
        self.solution[0][1] = 'in'
        self.solution[-1][-2] = 'out'

        return True

    # checking if it is safe to append to solution path.
    def is_safe_search(self, row, col):
        # if the row is out of index
        if row < 0 or row >= self.row_num:
            return False

        # if the column is out of index
        elif col < 0 or col >= self.col_num:
            return False

        # if the node is visited(True)
        elif self.visited[row][col]:
            return False

        # if the node is not blank, but a wall.
        elif self.maze[row][col] != 0:
            return False
        else:
            return True

    # search and store the solution path of current maze.
    def search(self, row, col):
        # mark to visited current node.
        self.visit(row, col)

        # SOLUTION REACHED : if solution path reached at exit of the maze, return True.
        if self.solution[row][col] == 'out':
            return True

        # add current node into total solution path. but if it is entrance, pass.
        if self.solution[row][col] != 'in':
            self.push_solution(row, col)

        # do depth-first search recursively.
        for path in direction:
            # CHECK PROMISING:
            # do search when only it is safe to search. if 4 directions is all not safe, current node is dead-end.
            if self.is_safe_search(row + path[0], col + path[1]):
                # if search method of child returned TRUE, the current node is part of solution.
                if self.search(row + path[0], col + path[1]):
                    return True

        # PRUNING AND BACKTRACKING:
        # dead end, there is no path left. remove current node from part of solution.
        self.pop_solution(row, col)
        return False

    # mark current node into visited node.
    def visit(self, row, col):
        self.visited[row][col] = True

    # mark current node into solution.
    def push_solution(self, row, col):
        self.solution[row][col] = True

    # mark current node into not solution.
    def pop_solution(self, row, col):
        self.solution[row][col] = False

    # check whether current node is safe to be part of maze or not.
    def is_safe_making(self, row, col, parent_direction):
        # if the row is out of index
        if row < 0 or row >= self.row_num:
            return False

        # if the column is out of index
        elif col < 0 or col >= self.col_num:
            return False

        # if it is the end of maze making
        elif self.solution[row][col] == 'out':
            return True

        # if the node is already visited, or border of maze
        elif self.maze[row][col] == (0 or 2):
            return False

        else:
            # if one of the neighboring node is already path, it can make a cycle or huge lump.
            # it may exist in real maze, but this program avoids it because it can make maze terrible.
            for path in direction:
                # ignore the path to parent node.
                if path[0] == -parent_direction[0] and path[1] == -parent_direction[1]:
                    continue
                # if neighboring node is already punched, current node is not safe.
                elif self.maze[row + path[0]][col + path[1]] == 0:
                    return False
            return True

    # make a stem path(solution path) at the maze.
    def make_stem(self, row, col, road):
        # make a path at current node, and add it to result path.
        self.punch(row, col)
        road.append((row, col))

        # to give a diversity to maze, shuffle the forwarding direction determining which node would be the next path.
        shuffled_path = list(copy.deepcopy(direction))
        random.shuffle(shuffled_path)

        # if making the stem of maze reached at the exit of maze, then make a branch.
        if self.solution[row][col] == 'out':
            # CHECK PROMISING :
            # if the result solution has an appropriate size, confirm it as a solution.
            if self.min_solution_size <= len(road) <= self.max_solution_size:

                # start at a random point of solution path.
                random.shuffle(road)
                for point in road:
                    for path in shuffled_path:
                        # start making new branch(fake path) by using random direction.
                        if self.is_safe_making(point[0] + path[0], point[1] + path[1], path):
                            # time-to-live, which means length of current branch.
                            random_ttl = random.randint(len(road) // 2, self.max_solution_size // 2)
                            # depth, which means max repeat number of recursive branch making.
                            random_depth = random.randint(self.min_depth, self.max_depth)

                            self.make_branch(point[0] + path[0], point[1] + path[1], [], random_ttl, random_depth)
                            break
                return True

            # PRUNING AND BACKTRACKING :
            # if the result solution doesn't have an appropriate size, get back to parent node.
            else:
                road.pop()
                self.recover(row, col)
                return False

        # another CHECK PROMISING and PRUNING:
        # if current path is too long to have an appropriate size when connected at the exit of maze, backtrack.
        elif self.max_solution_size - len(road) < (self.row_num - row + self.col_num - col) * 1.5:
            road.pop()
            self.recover(row, col)
            return False

        # do recursive call until it reaches at exit of maze.
        for path in shuffled_path:
            if self.is_safe_making(row + path[0], col + path[1], path):
                if self.make_stem(row + path[0], col + path[1], road):
                    return True
        # PRUNING AND BACKTRACKING :
        # dead end, there is no path left. remove current node from part of road.
        road.pop()
        self.recover(row, col)
        return False

    # it is quite similar with make_stem.
    # the difference is:
    # time_to_live (max length size of current branch)
    # depth (max number of recursive call of current branch)
    # if it reaches at the dead-end, it doesn't backtrack, but just end forwarding with a result.
    def make_branch(self, row, col, road, time_to_live, depth):
        # make a path at current node, and add it to result path.
        self.punch(row, col)
        road.append((row, col))

        # do making branch, only if there is a depth left.
        if depth > 0:

            # to give a diversity to maze, shuffle the forwarding direction,
            # determining which node would be the next path.
            shuffled_path = list(copy.deepcopy(direction))
            random.shuffle(shuffled_path)

            # do recursive call, only if there is a time_to_live left.
            if time_to_live > 0:
                for path in shuffled_path:
                    # if the next point is safe to make path, do the path forwarding.
                    if self.is_safe_making(row + path[0], col + path[1], path):
                        self.make_branch(row + path[0], col + path[1], road, time_to_live - 1, depth)
                        break

            # to give a diversity to maze, shuffle the forwarding direction and new start point
            # determining which node would be the next path.
            random.shuffle(road)
            random.shuffle(shuffled_path)

            for point in road:
                for path in shuffled_path:
                    # start making new branch(fake path) by using random direction, after checking if it is safe.
                    if self.is_safe_making(point[0] + path[0], point[1] + path[1], path):
                        random_ttl = random.randint(len(road), self.min_solution_size//1)
                        self.make_branch(point[0] + path[0], point[1] + path[1], [], random_ttl, depth - 1)
                        break

    # mark current node as a path.
    def punch(self, row, col):
        self.maze[row][col] = 0

    # mark current node as a wall.
    def recover(self, row, col):
        self.maze[row][col] = 1
