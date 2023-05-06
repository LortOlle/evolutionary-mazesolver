import random
import pygame
import numpy

class Agent:
    def __init__(self, genes, size):
        self.pos = (size/2, size/2)
        self.lastpos = (size/2, size/2)
        self.coords = (0,0)
        if type(genes) is int:
            self.genes = [random.choice([(-1,0), (0,1), (1,0), (0,-1)]) for n in range(genes)]
        elif type(genes) is list:
            self.genes = genes
        else:
            return ValueError
        self.direction = None
        self.done = False
        self.jitter = 0.2
        self.lerp = 0
        self.step = 0
        self.best = False
        self.visited = set([(0,0)])
        self.mutation = 0.01
        self.path = []
        
    
    def move(self, grid, size):
        if self.direction and not self.done:
            newx = round((1 - self.lerp) * self.lastpos[1] + self.lerp * self.direction[1])
            newy = round((1 - self.lerp) * self.lastpos[0] + self.lerp * self.direction[0])
            self.pos = (newy, newx)
            self.lerp += 0.2
            if self.best:
                self.path.append(self.pos)
            if self.lerp >= 1:
                self.direction = None
                self.lerp = 0
                self.step += 1
                self.lastpos = self.pos
                self.visited.add(self.coords)
            return 0
    
        else:
            if len(self.genes) > self.step:
                if self.coords == (len(grid)-1, len(grid[1]) -1):
                    self.done = True
                    return 1
                dir = self.genes[self.step]
                if 0 <= self.coords[1] + dir[1] < len(grid[0]) and 0 <= self.coords[0] + dir[0] < len(grid):
                    newcell = grid[ self.coords[0] + dir[0] ][ self.coords[1] + dir[1] ]
                    if newcell.wall:
                        self.direction = (round( (self.coords[0] + random.uniform(-self.jitter, self.jitter) * dir[0]) * size + size/2), 
                                          round( (self.coords[1] + random.uniform(-self.jitter, self.jitter) * dir[1]) * size + size/2))
                    else:
                        ydir = newcell.y + random.uniform(-self.jitter, self.jitter)
                        xdir = newcell.x + random.uniform(-self.jitter, self.jitter) 
                        new = numpy.array([ydir, xdir])
                        new = new * size + size/2
                        self.direction = tuple( numpy.rint(new) )
                        self.coords = (newcell.y, newcell.x)
                    return 0
                else:
                    self.direction = (round( (self.coords[0] + random.uniform(-self.jitter, self.jitter) * dir[0]) * size + size/2), 
                                      round( (self.coords[1] + random.uniform(-self.jitter, self.jitter) * dir[1]) * size + size/2))
                    return 0
            else:
                self.done = True
                return 1
            
    def fitness(self):
        score = sum(self.coords) * 3
        score += (len(self.genes) - self.step) * 10
        score += int(sum([sum(cell) for cell in self.visited]) / 3)
        return score
    
    def multiply(self):
        children = []
        for n in range(self.fitness() + 1):
            child = []
            for gene in self.genes:
                if random.random() < self.mutation:
                    child.append(random.choice([(-1,0), (0,1), (1,0), (0,-1)]))
                else:
                    child.append(gene)
            children.append(child)
        return children
    
    def draw(self, screen, size):
        
        if self.best:
            for dot in self.path:
                pygame.draw.circle(
                    screen,
                    (0,0,0),
                    (dot[1], dot[0]),
                    1
                )
            pygame.draw.circle(
                screen,
                (0,0,255),
                (self.pos[1], self.pos[0]),
                size / 5
            )
        else:
            pygame.draw.circle(
                screen,
                (255,0,255),
                (self.pos[1], self.pos[0]),
                size / 5
            )
        pygame.draw.circle(
                    screen,
                    (0,0,0),
                    (self.pos[1], self.pos[0]),
                    size/5,
                    2
                )
        
        
        