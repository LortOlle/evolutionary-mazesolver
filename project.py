from grid import Maze, Node
import pygame
from agent import Agent
import time
import random

def main():
    # Set the size of the maze and number of agents
    cols = 11
    rows = 9
    num_solvers = 10

    # The width of the cells is scaled to fit the screen
    w = int(600/max(cols,rows))

    # pygame and the screen is initialized
    pygame.init()
    screen = pygame.display.set_mode((cols * w, rows * w + 100))
    pygame.display.set_caption('Maze')

    # The maze object is initialized and top/left and bottom/right is set as start and goal
    maze = Maze(rows, cols)
    maze.grid[rows-1][0].state = 2
    maze.grid[0][cols-1].state = 3
    
    # The solver agents are initialized
    solvers = [Agent(rows*cols, w) for _ in range(num_solvers)]
    agents_running = False
    generation = 1
    running = True
    
    # Buttons are created
    font = pygame.font.Font(None, 36)
    agentbuttonText = font.render("Spawn Agents", True, (0,0,0))
    agentbuttonRect = pygame.Rect((20,rows*w + 20), (200, 60))
    resetbuttonText = font.render("Reset", True, (0,0,0))
    resetbuttonRect = pygame.Rect((240,rows*w + 20), (90, 60))
    stepRect = pygame.Rect((cols * w - 220,rows*w + 20), (200, 60))

    while running:
        # Handle exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0,0,0))
        # Draw maze
        maze.draw(screen, w)
        
        # Redraw the buttons
        pygame.draw.rect(screen,(200,200,200), agentbuttonRect, border_radius=5)
        screen.blit(agentbuttonText, (agentbuttonRect.x + 10, agentbuttonRect.y + 20))
        pygame.draw.rect(screen,(200,200,200), resetbuttonRect, border_radius=5)
        screen.blit(resetbuttonText, (resetbuttonRect.x + 10, resetbuttonRect.y + 20))
        
        # If the grid is leftclicked a wall is drawn
        leftclick, _,_ = pygame.mouse.get_pressed()
        if leftclick:
            x,y = pygame.mouse.get_pos()
            if y < rows * w and not agents_running:
                maze.grid[int(y/w)][int(x/w)].wall = True
                # If the wall blocked the only valid path to the goal it is removed
                if not maze.valid_grid():
                    maze.grid[int(y/w)][int(x/w)].wall = False
            else:
                # Press the spawn agent button
                if agentbuttonRect.x < x < agentbuttonRect.x + agentbuttonRect.width and agentbuttonRect.y < y < agentbuttonRect.y + agentbuttonRect.height and not agents_running:
                    agents_running = True
                # Press the reset button
                elif resetbuttonRect.x < x < resetbuttonRect.x + resetbuttonRect.width and resetbuttonRect.y < y < resetbuttonRect.y + agentbuttonRect.height:
                    maze = Maze(rows, cols)
                    maze.grid[rows-1][0].state = 2
                    maze.grid[0][cols-1].state = 3
                    
                    solvers = [Agent(rows*cols, w) for _ in range(num_solvers)]
                    agents_running = False
                    generation = 1
                    running = True
        
        # If agents are running we print the current generation and step
        if agents_running:
            sum = 0
            steptext = font.render(f"Gen {generation}: {solvers[0].step}/{rows*cols}", True, (170,170,170))
            screen.blit(steptext, (stepRect.x + 10, stepRect.y + 20))
            
            # Every agent gets moved and returns 1 if they are done and 0 if not
            for agent in solvers:
                sum += agent.move(maze.grid, w)
                agent.draw(screen, w)
            time.sleep(0.02)

            # When all agents are done moving we evolve
            if sum == num_solvers:
                # children is a list of possible agents for the next generation
                children = []
                generation +=1
                # We assume the first is the best and compare it to the rest
                best = solvers[0]
                for agent in solvers:
                    # Each agent adds a number of copys of itself equal to it's fitness to the children list 
                    children += agent.multiply()
                    # if an agent is better than the current best we make it the best
                    if agent.fitness() > best.fitness():
                        best = agent
                
                # The next generation is picked from the list of children
                solvers = [Agent(random.choice(children), w) for _ in range(num_solvers - 1)]
                # Last generations best is always added as the last child
                best = Agent(best.genes, w)
                best.best = True
                solvers.append(best)
                
                    

        # Update the display
        pygame.display.flip()

    pygame.quit()

    

if __name__ == "__main__":
    main()