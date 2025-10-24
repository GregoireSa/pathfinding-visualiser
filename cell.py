import pygame

# import necessary project files
import colours

pygame.init()


class Cell:
    
    def __init__(self, row: int, col: int, width: int, colour: tuple=colours.BLANK_COLOUR) -> None:

        # initialise attributes describing the cell's characteristics (dimensions, location, colour)
        self.row, self.col = row, col
        self.width = width
        self.x, self.y = self.col * self.width, self.row * self.width
        self.colour = colour
        self.rect = (self.x, self.y, self.width, self.width)

        # create a data structure to store all of the cell's neighbours
        self.neighbours = []
        self.prior_cell = None  # attribute to store the cell before itself in the final path 
        
        self.g_cost = float('inf')  # the cost from the start node to this cell
        self.h_cost = float('inf')  # the estimated cost from this cell to the target cell
        self.f_cost = float('inf')  # the g_cost + h_cost

    def draw(self, surface: pygame.Surface) -> None:

        pygame.draw.rect(surface, self.colour, self.rect)

    def update_costs(self) -> None:

        self.f_cost = self.h_cost + self.g_cost

    def update_neighbours(self, rows: int, cols: int, grid: list) -> None:
        """ updates the list of neighboring cells. """
        
        self.neighbours = []

        if self.row > 0:
            self.neighbours.append(grid[self.row-1][self.col])
        if self.row < rows - 1:
            self.neighbours.append(grid[self.row+1][self.col])
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col-1])
        if self.col < cols - 1:
            self.neighbours.append(grid[self.row][self.col+1])

