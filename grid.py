import pygame

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Node(y,x) for x in range(cols)] for y in range(rows)]
        self.color = [(255,255,255), (0,0,0)]
        self.start = self.grid[0][0]
        self.end = self.grid[rows-1][cols-1]

    def __str__(self):
        grid = ""
        for row in self.grid:
            for col in row:
                grid += f" {int(col.wall)} "
            grid += "\n"
        return grid[:-2]

    def draw(self, screen, size):
        for y in range(self.rows):
            for x in range(self.cols):
                color = self.color[self.grid[y][x].wall]
                pygame.draw.rect(
                    screen,
                    color,
                    (x * size + 1, y * size + 1, size-1, size-1)
                )
        pygame.draw.circle(
            screen,
            (0,255,0),
            (self.start.x * size + size/2, self.start.y * size + size/2), 
            size/4
        )
        pygame.draw.circle(
            screen,
            (255,0,0),
            (self.end.x * size + size/2, self.end.y * size + size/2), 
            size/4
        )
                
    def valid_grid(self):
        frontier = [self.start]
        visited = set()
        
        while frontier:
            curr = frontier.pop()
            visited.add(curr)
            for i,j in [(-1,0), (0,1), (1,0), (0,-1)]:
                if curr.x + j in range(self.cols) and curr.y + i in range(self.rows):
                    neighbor = self.grid[curr.y + i][curr.x + j]
                    if neighbor.wall == False and neighbor not in visited and neighbor not in frontier:
                        frontier.append(neighbor)
            if self.end in frontier:
                return True
        return False


class Node:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.wall = False