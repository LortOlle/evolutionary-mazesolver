# Evolutional Maze Solver
#### Video Demo:  <URL HERE>
#### Description:

## Intro
This project aims to create an agent capable of evolving from random instructions to a fully functional maze solver. In this project, we will explore the field of evolutionary algorithms and use them to train an agent to solve a randomly generated maze.

This readme gives a brief overview of the classes used and project itself.

## Project
The project itself initializes a pygame screen, a maze and a list of solver agents. The user can then draw walls in the grid to create a maze. As long as there exists a valid path from start to end the user can draw the maze in any way. When the user presses the "spawn agents" button the maze can no longer be changed and the solver agent will start randomly moving through it. They each get a set number of movements equal to the number of rows times the number of columns. This ensures that the agent theoretically could reach all cells in the maze. Once they have used up all steps they will reproduce, spawning new copies of themselves based on how well they performed. A small mutation rate ensures the agents keep evolving and doesn't get stuck.
## Maze
The Maze class keeps track of the grid. It has a number of rows and columns and a two-dimentional list filed with nodes (cells). These nodes has a x,y and "wall" parameter keeping track of where it is in the grid and if it is a wall in the maze or not. The maze also keeps track of a starting point and an end point. It has thee methods described below.

### __str__
the str method returns a string with 0s for paths and 1s for walls so you can display the maze by writing print(maze). This is just for debugging.

### draw
The draw method loops through the grid and displays walls as black rectangles and open paths as white. It takes a pygame sceen and a size as parameters to determine how large the squares should be drawn. It also draws a green circle at the starting square and a red circle at the end.

### valid_grid
When you draw the maze it should always be possible to finish it. The valid_grid method does a breadth first search of the grid to see if there is a path between the start and the end cell. This is to prevent the user from drawing an impossible maze.

## Agent
The agent class is the actual solver. It keeps track of its location both in pixels (self.pos) and row,colums (self.coords). The most important parameter is the self.genes list, which is initialized as a list of random touples of directions (up, right, down, left) coded as changes to self.coords. This starts off completely random but should evolve directions for actually solving a maze. It has more parameters but they are linked to the move and fitness method described below.

### move
The move method animates the movement of the agents in the grid. I wanted the agents to move smoothly between cells and not just teleport. The method first checks if the agent is currently on its way to a new cell by checking if it has a current "direction". If it has, it will keep moving by linear interpolation from one cell to the next in 10 steps. When it reaches its destination it will loose its "direction". If the agent does not have a direction it will first check if it's reached the goal. If it has it will just stay. If it hasn't it will instead take the next instruction in its gene and set that as its new direction. For visual interest I've added a "jitter" variable so the agents do not aim gor the center of a cell but instead a random coordinate at the center +- self.jitter.

### fitness
The fitness function calculates how well the agent performed once it's made all it's moves. The score is based on three things. The first is the sum of it's x and y coordinates in the grid times three, which is because the goal is at the bottom right, and we want to reinforce movement down and right. The second part is the difference between the moves and number of steps taken times ten, which will be zero for any agent that doesn't make it to the goal because the agent has taken as many steps as there are moves. This will greatly reward any agent that makes it to the end. The third and last part is the sum of the x and y coordinates of all visited cells divided by three. This is to encourage exploration and reward exploration closer to the end more. The total fitness is the sum of these three parts.

### multiply
The multiply function will create a "child" for each fitness point. Each child copies the moves from the parents except for a one percent chance that it instead gets a random move. This is the mutation that prevent the agents to evolve into the same moveset. The next generation of agents are picked from the list of children making agents with higher fitness more likely to be picked.

### draw
The last function draws the agents as a pink circle. If the agent is the current best it will instead be drawn as blue. Additionally the current best will also have it's path drawn as a line of dots.