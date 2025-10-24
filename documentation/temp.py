import pygame
import random
from typing import Callable

import cell
import basicUI
import colours

pygame.init()


class Visualisation:

    
    def __init__(self, surface: pygame.Surface, width: int, height: int,
                 menu_func: Callable, cell_size: int=10) -> None:

        self.surface = surface
        self.width, self.height = width, height
        self.grid_width = 0.75 * self.width
        self.ui_width = self.width - self.grid_width
        self.menu_func = menu_func

        self.grid = []
        self.cell_size = cell_size
        self.rows = int(self.height // self.cell_size)
        self.cols = int(self.grid_width // self.cell_size)

        self.init_grid()
        self.start_cell = None
        self.finish_cell = None

        self.buttons = []

        self.reset_button = basicUI.Button(self.surface, "Reset", self.reset_grid, (0, 0),
                                           fg=colours.UI_TEXT_COLOUR, bg=colours.UI_BUTTON_COLOUR)
        self.reset_button.center = (width - (self.ui_width // 2), 350)
        self.buttons.append(self.reset_button)

        self.random_button = basicUI.Button(self.surface, "Random", self.random_func, (0, 0),
                                            fg=colours.UI_TEXT_COLOUR, bg=colours.UI_BUTTON_COLOUR)
        self.random_button.center = (width - (self.ui_width // 2), 400)
        self.buttons.append(self.random_button)

        self.menu_button = basicUI.Button(self.surface, "Menu [key]", self.menu_func, (0, 0),
                                          fg=colours.UI_TEXT_COLOUR, bg=colours.UI_BUTTON_COLOUR)
        self.menu_button.center = (width - (self.ui_width // 2), 450)
        self.buttons.append(self.menu_button)

    def init_grid(self) -> None:
        """ Creates the grid when the visualisation page is first ran """
        
        self.grid = []

        for i in range(self.rows):

            self.grid.append([])

            for j in range(self.cols):

                self.grid[i].append(cell.Cell(i, j, self.cell_size))

                if i == 0 or j == 0 or i == self.rows - 1 or j == self.cols - 1:
                    self.grid[i][j].colour = colours.BORDER_COLOUR

        for row in self.grid:
            for node in row:
                node.update_neighbours(self.rows, self.cols, self.grid)

    def reset_grid(self) -> None:
        """ Resets all cells (except for borders) to blank cells """

        for row in self.grid:
            for node in row:
                if node.colour != colours.BLANK_COLOUR and node.colour != colours.BORDER_COLOUR:
                    node.colour = colours.BLANK_COLOUR

    def random_func(self) -> None:
        """ Sets a random amount of cells to barriers """
        
        for row in self.grid:
            for node in row:
                chance = random.randint(1, 15)
                if (node.colour == colours.BLANK_COLOUR or node.colour == colours.PATH_COLOUR) and chance == 1:
                    node.colour = colours.BARRIER_COLOUR

    def in_bounds(self, x: int, y:int, mouse_pos: tuple) -> bool:
        """ Checks if a clicked_node coordinate is on the grid """
        
        if mouse_pos[0] >= self.grid_width or mouse_pos[1] >= self.height or mouse_pos[1] <= 0 or mouse_pos[0] <= 0:
            return False
        
        if x == 0 or y == 0 or x == self.cols - 1 or y == self.rows - 1:
            return False
        
        return True

    def check_grid(self, colour: tuple) -> cell.Cell:
        """ Checks if a certain type of cell (by colour) is on the grid """

        for row in self.grid:
            for node in row:
                if node.colour == colour:
                    return node

    def draw_grid(self) -> None:
        """ Draws the grid on the visualisation page """

        for row in self.grid:
            for node in row:
                node.draw(self.surface)

        for i in range(self.cols):
            pygame.draw.line(self.surface, colours.GRID_LINES_COLOUR,
                             (i * self.cell_size, 0), (i * self.cell_size, self.height))

        for j in range(self.rows):
            pygame.draw.line(self.surface, colours.GRID_LINES_COLOUR,
                             (0, j * self.cell_size), (self.grid_width, j * self.cell_size))

    def load(self) -> None:
        """ Checks for any interactions with elements or keys and
        checks if the user has added nodes to the grid """

        self.start_cell = self.check_grid(colours.START_COLOUR)
        self.finish_cell = self.check_grid(colours.FINISH_COLOUR)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.menu_func()
        if keys[pygame.K_r]:
            self.reset_grid()

        if pygame.mouse.get_pressed():

            mouse_pos = pygame.mouse.get_pos()
            x_coord = mouse_pos[0] // self.cell_size
            y_coord = mouse_pos[1] // self.cell_size

            if pygame.mouse.get_pressed()[0] and self.in_bounds(x_coord, y_coord, mouse_pos):

                clicked_node = self.grid[y_coord][x_coord]
                
                if clicked_node.colour != colours.QUEUED_COLOUR and clicked_node.colour != colours.VISITED_COLOUR:
                    
                    # if the start node is not on the grid, then the next click will be a start node
                    if not self.check_grid(colours.START_COLOUR):
                        clicked_node.colour = colours.START_COLOUR

                    # if the start node is on the grid but there is no finish node, then the next click will be a finish node
                    elif not self.check_grid(colours.FINISH_COLOUR) and clicked_node.colour != colours.START_COLOUR: 
                        clicked_node.colour = colours.FINISH_COLOUR

                    # if the start node and finish node are already on the grid then the next click will be a barrier node
                    elif clicked_node.colour != colours.START_COLOUR and clicked_node.colour != colours.FINISH_COLOUR:
                        clicked_node.colour = colours.BARRIER_COLOUR

            elif pygame.mouse.get_pressed()[2] and self.in_bounds(x_coord, y_coord, mouse_pos):

                clicked_node = self.grid[y_coord][x_coord]
                
                if clicked_node.colour != colours.QUEUED_COLOUR and clicked_node.colour != colours.VISITED_COLOUR:
                    
                    clicked_node.colour = colours.BLANK_COLOUR

        self.surface.fill(colours.UI_BG_COLOUR)
        self.grid[0][0].colour = colours.VISITED_COLOUR
        self.draw_grid()

        basicUI.text(self.surface, "PATHFINDING", (self.width - (self.ui_width // 2), 30), colours.UI_TEXT_COLOUR, 50)

        self.stop_button.update()
        for button in self.buttons:

            if not self.is_running:
                button.update()

            button.draw()