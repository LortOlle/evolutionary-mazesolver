import pytest
from grid import Maze, Node
from agent import Agent

def test_valid_grid():
    maze = Maze(3, 3)
    maze.grid[1][0].wall = True  # Add a wall to block the path
    maze.grid[1][1].wall = True
    maze.grid[1][2].wall = True
    assert not maze.valid_grid()  # Check that the grid is no longer valid
    
def test_multiply():
    agent = Agent(10, 5)
    children = agent.multiply()
    assert len(children) == agent.fitness() + 1  # Check that the number of children is correct
    assert all(len(child) == len(agent.genes) for child in children)  # Check that all children have the same number of genes

def test_node_creation():
    node = Node(2, 3)
    assert node.y == 2
    assert node.x == 3
    assert not node.wall

def test_maze_creation():
    maze = Maze(10, 10)
    assert maze.rows == 10
    assert maze.cols == 10
    assert len(maze.grid) == 10
    assert len(maze.grid[0]) == 10
    assert isinstance(maze.grid[5][5], Node)