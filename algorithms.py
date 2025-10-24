import pygame
import time

# import necessary project files
import colours
from cell import Cell

pygame.init()


class Dijkstra:
    """
    This class provides functionality for running Dijkstra's algorithm on a grid to find
    the shortest path from a start cell to a finish cell.
    
    Attributes:
    
        surface (pygame.Surface): The surface on which the grid is displayed.
        page: The current page of the program.
        grid (list): the grid on which the algorithm is to be run.
        
    Methods:
    
        check_neighbours(self, cell: Cell) -> None:
            Checks if the cell has any neighbours
        run(self, start_cell: Cell, finish_cell: Cell) -> str
            Runs Dijkstra's algorithm to find the shortest path.
            Args:
                start_cell (Cell): The starting cell of the path.
                finish_cell (Cell): The ending cell of the path.
            Returns:
                str: A message indicating whether the path was found and its length and time taken.
            Raises:
                ValueError: If the start_cell or finish_cell is not placed on the grid.
    
    """
    
    def __init__(self, surface: pygame.Surface, page, grid: list) -> None:

        # initialise all attributes necessary to load the display
        self.surface = surface
        self.page = page
        
        # initialise attributes used in the pathfinding algorithm
        self.grid = grid
        self.open = []
        self.is_found = False

        # initialise useful data to help with analysis
        self.path_length = 0
        self.nodes_searched = 0

    def check_neighbours(self, cell: Cell) -> None:
        """ Checks if the cell has any neighbours that have not been visited yet """
        
        # loops through all of the current cell's neighbours
        for neighbour in cell.neighbours:
            
            # checks if the neighbour's colour is blank or finished
            if neighbour.colour == colours.BLANK_COLOUR or neighbour.colour == colours.FINISH_COLOUR:

                # add the neighbour to the open set, set it to queued, and set its prior cell to the current cell
                self.open.append(neighbour)
                neighbour.colour = colours.QUEUED_COLOUR
                neighbour.prior_cell = cell

    def run(self, start_cell: Cell, finish_cell: Cell) -> str:
        
        if start_cell and finish_cell:
            
            # reset any visited/queued cells to blank
            for row in self.grid:
                for node in row:
                    if node.colour == colours.VISITED_COLOUR or node.colour == colours.QUEUED_COLOUR:
                        node.colour = colours.BLANK_COLOUR
            
            # initialise variables
            self.path_length = 0
            self.nodes_searched = 1

            self.open = [start_cell]
            self.is_found = False
            self.page.is_running = True

            self.start_time = time.time()

            # reset any path cells from previous algorithms
            for row in self.grid:
                for node in row:
                    if node.colour == colours.PATH_COLOUR:
                        node.colour = colours.BLANK_COLOUR

            # ensures that the loop only runs if there are still nodes to explore
            while self.open and self.page.is_running:
                
                self.nodes_searched += 1
                
                # check if the user wants to quit the program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # sets the current cell to the first unvisited cell in the open list and checks if it is the finish cell
                curr_cell = self.open[0]
                if curr_cell == finish_cell:
                    self.is_found = True
                    self.elapsed_time = round(time.time() - self.start_time, 3)
                    return self.backtrack(start_cell, finish_cell)

                self.check_neighbours(curr_cell)

                # set newly visited cells to visited and ensure that the start cell has the correct colour
                curr_cell.colour = colours.VISITED_COLOUR
                start_cell.colour = colours.START_COLOUR

                # remove the current cell from the open list and load the screen (visualisation page)
                self.open.pop(0)
                self.page.load()
                pygame.display.update()
            
            self.page.is_running = False
            return "path not found"
                
        else:
            return "start/finish cell not placed"
                
    def backtrack(self, start_cell: Cell, finish_cell: Cell) -> str:
        
        # reset any visited/queued cells to blank
        for row in self.grid:
            for node in row:
                if node.colour == colours.VISITED_COLOUR or node.colour == colours.QUEUED_COLOUR:
                    node.colour = colours.BLANK_COLOUR

        if self.is_found:

            finish_cell.colour = colours.FINISH_COLOUR
            curr_cell = finish_cell.prior_cell

            while True:

                self.path_length += 1

                # check if the user wants to quit the program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # exit the loop if the algorithm has found the path
                if curr_cell == start_cell:
                    break
                
                # backtrack to the previous cell and load the screen (visualisation page)
                curr_cell.colour = colours.PATH_COLOUR
                curr_cell = curr_cell.prior_cell

                self.page.load()
                pygame.display.update()

        self.page.is_running = False

        # output an appropriate message
        
        if not self.is_found:
            return "path not found"
        else:
            return f"[ Dijkstra ] visited {self.nodes_searched} nodes, path length = {self.path_length}," \
                f" time taken = {self.elapsed_time}s"


class AStar:
    """
    This class provides functionality for running the A* algorithm on a grid to find
    the shortest path from a start cell to a finish cell.
    
    Attributes:
    
        surface (pygame.Surface): The surface on which the grid is displayed.
        page: The current page of the program.
        grid (list): the grid on which the algorithm is to be run.
        
    Methods:

        best_node(self) -> Cell:
            Returns the cell with the lowest f_cost in the open list
        check_neighbours(self, cell: Cell) -> None:
            Adds any new neighbours to the open list and updates costs
        run(self, start_cell: Cell, finish_cell: Cell) -> str
            Runs the A* algorithm to find the shortest path.
            Args:
                start_cell (Cell): The starting cell of the path.
                finish_cell (Cell): The ending cell of the path.
            Returns:
                str: A message indicating whether the path was found and its length and time taken.
            Raises:
                ValueError: If the start_cell or finish_cell is not placed on the grid.
    
    """
    
    def __init__(self, surface: pygame.Surface, page, grid: list) -> None:

        # initialise all attributes necessary to load the display
        self.surface = surface
        self.page = page
        
        # initialise attributes used in the pathfinding algorithm
        self.grid = grid
        self.open = []
        self.visited = []
        self.is_found = False

        # initialise useful data to help with analysis
        self.path_length = 0
        self.nodes_searched = 0

    def best_node(self) -> Cell:
        """ Returns the cell with the lowest f_cost in the open list """

        best = []  # stores all of the cells with the best f_cost
        best_f_cost = float('inf')  # stores the value of the best f_cost

        # loops through all nodes currently in the open set
        for node in self.open:
            # appends the node to the best array if it is equal to the current best f_cost
            if node.f_cost == best_f_cost:
                best.append(node)
            # resets the best array to just the node if a new best f_cost is found
            elif node.f_cost < best_f_cost:
                best = [node]
                best_f_cost = node.f_cost

        # if only 1 cell has the best f_cost, then return the cell
        if len(best) == 1:
            return best[0]
        # otherwise return the cell with the best g_cost (out of the cells with the best f_cost)
        else:
            return min(best, key=lambda node: node.g_cost)
            

    def check_neighbours(self, cell: Cell) -> None:
        """ Adds any new neighbours to the open list and updates costs """
        
        # loops through all of the current cell's neighbours
        for neighbour in cell.neighbours:

            # checks if the neighbour's colour is blank or finished
            if neighbour.colour == colours.BLANK_COLOUR or neighbour.colour == colours.FINISH_COLOUR:
                
                # checks whether the g_cost via the current cell is lower than the neighbour's current g_cost
                if cell.g_cost + 1 < neighbour.g_cost:
                    # updates the g_cost and prior cell
                    neighbour.g_cost = cell.g_cost + 1
                    neighbour.prior_cell = cell
                    # updates the neighbour's f_cost after the change in g_cost
                    neighbour.update_costs()

                    # if the cell has not yet been seen, add it to the open set
                    if neighbour not in self.open and neighbour not in self.visited:
                        self.open.append(neighbour)

                # make the cell queued
                neighbour.colour = colours.QUEUED_COLOUR
        

    def run(self, start_cell: Cell, finish_cell: Cell) -> str:
        
        if start_cell and finish_cell:

            # reset any visited/queued cells to blank
            for row in self.grid:
                for node in row:
                    if node.colour == colours.VISITED_COLOUR or node.colour == colours.QUEUED_COLOUR:
                        node.colour = colours.BLANK_COLOUR
            
            # initialise variables
            self.path_length = 0
            self.nodes_searched = 1

            self.open = [start_cell]
            self.is_found = False
            self.page.is_running = True

            self.start_time = time.time()

            start_cell.g_cost = 0
            start_cell.update_costs()

            # reset costs and any path cells from previous algorithms
            for row in self.grid:
                for node in row:

                    node.h_cost = abs(node.row - finish_cell.row) + abs(node.col - finish_cell.col)

                    if node != start_cell:
                        node.g_cost = float('inf')

                    node.update_costs()

                    if node.colour == colours.PATH_COLOUR:
                        node.colour = colours.BLANK_COLOUR

            # ensures that the loop only runs if there are still nodes to explore
            while self.open and self.page.is_running:
                
                self.nodes_searched += 1
                
                # check if the user wants to quit the program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # sets the current cell to the cell with the lowest f_cost in the open list and checks if it is the finish cell
                curr_cell = self.best_node()
                if curr_cell == finish_cell:
                    self.is_found = True
                    self.elapsed_time = round(time.time() - self.start_time, 3)
                    return self.backtrack(start_cell, finish_cell)

                self.check_neighbours(curr_cell)

                # remove the current cell from the open list and load the screen (visualisation page)
                curr_cell.colour = colours.VISITED_COLOUR
                start_cell.colour = colours.START_COLOUR
                self.open.remove(curr_cell)

                # load the screen
                self.page.load()
                pygame.display.update()
            
            return "path not found"
        
        else:
            return "start/finish cell not placed"

    def backtrack(self, start_cell: Cell, finish_cell: Cell) -> str:

        # reset any visited/queued cells to blank
        for row in self.grid:
            for node in row:
                if node.colour == colours.VISITED_COLOUR or node.colour == colours.QUEUED_COLOUR:
                    node.colour = colours.BLANK_COLOUR

        if self.is_found:

            finish_cell.colour = colours.FINISH_COLOUR
            curr_cell = finish_cell.prior_cell

            while True:

                self.path_length += 1

                # check if the user wants to quit the program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # exit the loop if the algorithm has found the path
                if curr_cell == start_cell:
                    break
                
                # backtrack to the previous cell and load the screen (visualisation page)
                curr_cell.colour = colours.PATH_COLOUR
                curr_cell = curr_cell.prior_cell

                self.page.load()
                pygame.display.update()

        self.page.is_running = False
        
        # output an appropriate message
        if not self.is_found:
            return "path not found"
        else:
            return f"[    A*    ] visited {self.nodes_searched} nodes, path length = {self.path_length}," \
                f" time taken = {self.elapsed_time}s"


class GreedyBFS:
    """
    This class provides functionality for running the greedy BFS algorithm on a grid to efficiently find
    a path from a start cell to a finish cell.
    
    Attributes:
    
        surface (pygame.Surface): The surface on which the grid is displayed.
        page: The current page of the program.
        grid (list): the grid on which the algorithm is to be run.
        
    Methods:

        check_neighbours(self, cell: Cell) -> None:
            Adds any new neighbours to the open list
        best_cost(self) -> Cell:
            Returns the cell with the lowest h_cost in the open list
        run(self, start_cell: Cell, finish_cell: Cell) -> str
            Runs the greedy BFS algorithm to find the shortest path.
            Args:
                start_cell (Cell): The starting cell of the path.
                finish_cell (Cell): The ending cell of the path.
            Returns:
                str: A message indicating whether the path was found and its length and time taken.
            Raises:
                ValueError: If the start_cell or finish_cell is not placed on the grid.
    
    """

    def __init__(self, surface: pygame.Surface, page, grid: list) -> None:

        # initialise all attributes necessary to load the display
        self.surface = surface
        self.page = page
        
        # initialise attributes used in the pathfinding algorithm
        self.grid = grid
        self.open = []
        self.is_found = False

        # initialise useful data to help with analysis
        self.nodes_searched = 0
        self.path_length = 0
    
    def check_neighbours(self, cell: Cell) -> None:
        """ Adds any new neighbours to the open list """
        
        # loops through all of the current cell's neighbours
        for neighbour in cell.neighbours:

            # checks if the neighbour's colour is blank or finished
            if neighbour.colour == colours.BLANK_COLOUR or neighbour.colour == colours.FINISH_COLOUR:

                # adds the neighbour to the open list and sets its colour to queued
                self.open.append(neighbour)
                neighbour.colour = colours.QUEUED_COLOUR
                # sets the neighbour's prior cell to the current cell
                neighbour.prior_cell = cell

    
    def best_cost(self) -> Cell:
        """ Returns the cell with the lowest h_cost in the open list """

        return min(self.open, key=lambda node: node.h_cost)

    def run(self, start_cell: Cell, finish_cell: Cell) -> str:
        """Runs the greedy BFS algorithm on the grid to efficiently find a path from the start_cell to the finish_cell.

        Args:
            start_cell (Cell): The starting cell of the path.
            finish_cell (Cell): The ending cell of the path.

        Returns:
            str: A message indicating whether the path was found and its length and time taken.

        Raises:
            ValueError: If the start_cell or finish_cell is not placed on the grid.
        """
        
        if start_cell and finish_cell:

            # reset any visited/queued cells to blank
            for row in self.grid:
                for node in row:
                    if node.colour == colours.VISITED_COLOUR or node.colour == colours.QUEUED_COLOUR:
                        node.colour = colours.BLANK_COLOUR

            # initialise variables
            self.nodes_searched = 1
            self.path_length = 0

            self.open = [start_cell]
            self.is_found = False
            self.page.is_running = True

            self.start_time = time.time()

            # reset h_costs and any path cells from previous algorithms
            for row in self.grid:
                for node in row:
                    node.h_cost = abs(node.row - finish_cell.row) + abs(node.col - finish_cell.col)
                    if node.colour == colours.PATH_COLOUR:
                        node.colour = colours.BLANK_COLOUR

            # ensures that the loop only runs if there are still nodes to explore
            while self.open and self.page.is_running:

                self.nodes_searched += 1

                # checks if the user wants to quit the program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                
                # sets the current cell to the cell with the lowest h_cost in the open list and checks if it is the finish cell
                curr_cell = self.best_cost()
                if curr_cell == finish_cell:
                    self.is_found = True
                    self.elapsed_time = round(time.time() - self.start_time, 3)
                    return self.backtrack(start_cell, finish_cell)

                self.check_neighbours(curr_cell)

                # set newly visited cells to visited and remove the current cell from the open list
                curr_cell.colour = colours.VISITED_COLOUR
                start_cell.colour = colours.START_COLOUR

                self.open.remove(curr_cell)

                # load the screen (visualisation page)
                self.page.load()
                pygame.display.update()
            
            return "path not found"
        
        else:
            return "start/finish cell not placed"


    def backtrack(self, start_cell, finish_cell) -> str:
        
        # reset any visited/queued cells to blank
        for row in self.grid:
            for node in row:
                if node.colour == colours.VISITED_COLOUR or node.colour == colours.QUEUED_COLOUR:
                    node.colour = colours.BLANK_COLOUR

        if self.is_found:

            finish_cell.colour = colours.FINISH_COLOUR
            curr_cell = finish_cell.prior_cell

            while True:

                self.path_length += 1

                # check if the user wants to quit the program
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                # exit the loop if the algorithm has found the path
                if curr_cell == start_cell:
                    break
                
                # backtrack to the previous cell and load the screen (visualisation page)
                curr_cell.colour = colours.PATH_COLOUR
                curr_cell = curr_cell.prior_cell

                self.page.load()
                pygame.display.update()

        self.page.is_running = False
        
        # output an appropriate message
        
        if not self.is_found:
            return "path not found"
        else:
            return f"[Greedy BFS] visited {self.nodes_searched} nodes, path length = {self.path_length}," \
                f" time taken = {self.elapsed_time}s"