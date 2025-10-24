import pygame
import webbrowser
import random
from typing import Callable

import basicUI

pygame.init()

width, height = 1000, 500
grid_width = width * 0.75
ui_width = width - grid_width
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

cell_size = 25
rows = int(height // cell_size)
cols = int(grid_width // cell_size)
grid = []

# COLOURS:
UI_BG_COLOUR = (50, 50, 50)
UI_BUTTON_COLOUR = (60, 60, 60)
UI_TEXT_COLOUR = (100, 100, 100)

GRID_LINES_COLOUR = (50, 50, 50)
BARRIER_COLOUR = (100, 100, 100)
BORDER_COLOUR = (65, 65, 65)
BLANK_COLOUR = (20, 20, 20)
START_COLOUR = (97, 135, 40)
FINISH_COLOUR = (178, 16, 49)

QUEUED_COLOUR = (0, 100, 100)
VISITED_COLOUR = (5, 5, 5)
PATH_COLOUR = (128, 51, 135)


class Cell:
    
    def __init__(self, row: int, col: int, width: int, colour: tuple=BLANK_COLOUR) -> None:

        # initialise attributes describing the cell's characteristics (dimensions, location, colour)
        self.row, self.col = row, col
        self.width = width
        self.x, self.y = self.col * self.width, self.row * self.width
        self.colour = colour
        self.rect = (self.x, self.y, self.width, self.width)

        # create a data structure to store all of the cell's neighbours
        self.neighbours = []

    def draw(self, surface: pygame.Surface) -> None:

        # draw the cell onto the grid at its designated coordinates
        pygame.draw.rect(surface, self.colour, self.rect)

    def update_neighbours(self, rows: int, cols: int, grid: list) -> None:
        """ updates the list of neighboring cells. """
        
        # reset the neighbours data structure to remove any neighbours that may have previously been added
        self.neighbours = []

        # ensure that the neighbour is on the grid, and is not outside the borders
        if self.row > 0:
            self.neighbours.append(grid[self.row-1][self.col])
        if self.row < rows - 1:
            self.neighbours.append(grid[self.row+1][self.col])
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col-1])
        if self.col < cols - 1:
            self.neighbours.append(grid[self.row][self.col+1])


def docs_func() -> None:
    
    webbrowser.open("https://docs.google.com/document/d/1U96vEvA0jDv8XYHGnGShQUluY2gDUlA39RXWsx02tb4/edit")

def quit_func() -> None:
    
    pygame.quit()
    quit()

def menu(width: int, height: int, main_func: Callable) -> None:
    
    margin = 5
    menu_buttons = []

    start_button = basicUI.Button(win, "START", main_func, (0, 0), fontsize=60,
                                        fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    start_button.center = (width // 2, height // 2 - start_button.button_rect.height // 2 - margin)
    menu_buttons.append(start_button)

    quit_button = basicUI.Button(win, "QUIT", quit_func, (0, 0), fontsize=60,
                                        fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    quit_button.center = (width // 2, height // 2 + start_button.button_rect.height // 2 + margin)
    menu_buttons.append(quit_button)

    docs_button = basicUI.Button(win, "DOCS", docs_func, (0, 0), fontsize=20,
                                        fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    docs_button.center = (width - docs_button.button_rect.width // 2 - margin*2,
                                docs_button.button_rect.height // 2 + margin*2)
    menu_buttons.append(docs_button)
    
    running = True
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        win.fill(UI_BG_COLOUR)
        
        for button in menu_buttons:
            button.draw()
            button.update()
        
        pygame.display.update()
        
    pygame.quit()
    quit()
    

def draw_surface(buttons) -> None:
    
    # fill the screen with the BG colour (to remove previously drawn objects from the window)
    win.fill(UI_BG_COLOUR)
    
    # loop through all nodes on the grid
    for row in grid:
        for node in row:
            # draw the node onto the window
            node.draw(win)
    
    # draw lines to separate columns
    for i in range(cols + 1):
        pygame.draw.line(win, GRID_LINES_COLOUR, (i * cell_size, 0), (i * cell_size, height))

    # draw lines to separate rows
    for j in range(rows + 1):
        pygame.draw.line(win, GRID_LINES_COLOUR, (0, j * cell_size), (grid_width, j * cell_size))
    
    # write "PATHFINDING" at the top of the sidebar
    basicUI.text(win, "PATHFINDING", (width - (ui_width // 2), 50), UI_TEXT_COLOUR, 40)
    
    # draw and update all buttons
    for button in buttons:
        button.update()
        button.draw()
    
    # update the window
    pygame.display.update()


def init_grid() -> None:
    # give the function access to the global data structure 'grid'
    global grid
    
    # reset the grid to remove any previously added cells
    grid = []

    # loop for the amount of rows in the grid
    for i in range(rows):

        # add an empty array to the grid to represent a row
        grid.append([])

        # loop for the amount of columns in the grid
        for j in range(cols):

            # create a new instance of the cell class at the required row and column, and add it to the grid data structure
            grid[i].append(Cell(i, j, cell_size))

            # if the cell is on the border, then set the cell's colour to BORDER_COLOUR
            if i == 0 or j == 0 or i == rows - 1 or j == cols - 1:
                grid[i][j].colour = BORDER_COLOUR

def in_bounds(x: int, y: int, mouse_pos: tuple) -> bool:
    """ Checks if a clicked_node coordinate is on the grid """
    
    # check if the mouse's current position is on the window, and on the grid (instead of the UI sidebar)
    if mouse_pos[0] >= grid_width or mouse_pos[1] >= height or mouse_pos [1] <= 0 or mouse_pos[0] <= 0:
        return False
    # check if the mouse is on the area of the grid where the user can draw (i.e. not on the border)
    if x == 0 or y == 0 or x == cols - 1 or y == rows - 1:
        return False
    # otherwise return true, since the cursor must be within the drawable section of the grid
    return True

def check_grid(colour: tuple) -> bool:
    """ Checks if a certain type of cell (by colour) is on the grid """

    # loop through all nodes on the grid
    for row in grid:
        for node in row:
            # check if the colour of the node being checked is the same as the colour being searched for
            if node.colour == colour:
                return True
    # if none of the cells matched, then the colour must not be on the grid
    return False

def check_clicks() -> None:

    # check if the mouse is being pressed
    if pygame.mouse.get_pressed():

            # get the mouse's coordinates, and its relative coordinates on the grid
            mouse_pos = pygame.mouse.get_pos()
            x_coord = mouse_pos[0] // cell_size
            y_coord = mouse_pos[1] // cell_size

            # check if the click was a left click, and whether the mouse's coordinates are on the grid (in bounds)
            if pygame.mouse.get_pressed()[0] and in_bounds(x_coord, y_coord, mouse_pos):
                
                # get the cell that was clicked
                clicked_node = grid[y_coord][x_coord]
                
                # ensure that the clicked cell is not queued or visited (during algorithm runtime)
                if clicked_node.colour != QUEUED_COLOUR and clicked_node.colour != VISITED_COLOUR:
                    
                    # if the start node is not on the grid, then the next click will be a start node
                    if not check_grid(START_COLOUR):
                        clicked_node.colour = START_COLOUR

                    # if the start node is on the grid but there is no finish node, then the next click will be a finish node
                    elif not check_grid(FINISH_COLOUR) and clicked_node.colour != START_COLOUR: 
                        clicked_node.colour = FINISH_COLOUR

                    # if the start node and finish node are already on the grid then the next click will be a barrier node
                    elif clicked_node.colour != START_COLOUR and clicked_node.colour != FINISH_COLOUR:
                        clicked_node.colour = BARRIER_COLOUR

            # check if the click was a right click, and whether the mouse's coordinates are on the grid (in bounds)
            elif pygame.mouse.get_pressed()[2] and in_bounds(x_coord, y_coord, mouse_pos):
                
                # get the cell that was clicked
                clicked_node = grid[y_coord][x_coord]
                
                # ensure that the clicked cell is not queued or visited (during algorithm runtime)
                if clicked_node.colour != QUEUED_COLOUR and clicked_node.colour != VISITED_COLOUR:
                    
                    # reset the cell to blank
                    clicked_node.colour = BLANK_COLOUR

def reset_grid() -> None:
    
    # loop through all nodes on the grid
    for row in grid:
        for node in row:
            # ensure that the cell is not a border cell or already blank
            if node.colour != BLANK_COLOUR and node.colour != BORDER_COLOUR:
                    # reset the cell to a blank colour
                    node.colour = BLANK_COLOUR
                    
def random_func() -> None:
    
    # loop through all nodes on the grid
    for row in grid:
        for node in row:
            # set the chance of a cell becoming random
            chance = random.randint(1, 15)
            # check that the cell is blank or a path, and that the chance is 1
            if (node.colour == BLANK_COLOUR or node.colour == PATH_COLOUR) and chance == 1:
                node.colour = BARRIER_COLOUR

def main() -> None:
    
    # create a data structure to store all buttons on the UI sidebar
    main_buttons = []
    
    # create a button to reset the grid and add it to the main_buttons data structure
    reset_button = basicUI.Button(win, "Reset", reset_grid, (0, 0),
                                           fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    reset_button.center = (width - (ui_width // 2), (height // 2))
    main_buttons.append(reset_button)

    # create a button to randomise the grid and add it to the main_buttons data structure
    random_button = basicUI.Button(win, "Random", random_func, (0, 0),
                                        fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    random_button.center = (width - (ui_width // 2), (height // 2) + 50)
    main_buttons.append(random_button)

    # create a button to return to the menu and add it to the main_buttons data structure
    menu_button = basicUI.Button(win, "Menu", lambda: menu(width, height, main), (0, 0),
                                        fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    menu_button.center = (width - (ui_width // 2), (height // 2) - 50)
    main_buttons.append(menu_button)

    # create the grid data structure when the program is first run
    init_grid()
    running = True
    
    # loop through main loop until running is False
    while running:
        
        # check if the user wants to quit the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # check if the user has clicked, and draw the surface
        check_clicks()
        draw_surface(main_buttons)

    # if the program is not running, quit pygame and the program
    pygame.quit()
    quit()


# only run the 'main' subroutine if the file running it is the current file
if __name__ == '__main__':
    
    menu(width, height, main)