import pygame

# import necessary project files
import menu
import visualisation

pygame.init()


def event_handler() -> None:
    """ Handles pygame events """

    for event in pygame.event.get():
        # checks if the user wants to quit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


class PageManager:
    """ Handles page switching (between main and visualisation) """
    
    def __init__(self) -> None: 
        self.curr_page = 0
    
    def to_menu(self) -> None:
        self.curr_page = 0
    
    def to_visualisation(self) -> None:
        self.curr_page = 1


def main(cell_size) -> None: 
    """ Controls which page is currently displayed and runs the main loop"""
    
    # initialise display variables

    width, height = 1000, 500

    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pathfinding coursework")
    clock = pygame.time.Clock()
    FPS = 60
    
    page_manager = PageManager()

    # allocate menu and visualisation pages to variables
    menu_page = menu.Menu(win, width, height, page_manager.to_visualisation)
    visualisation_page = visualisation.Visualisation(win, width, height, page_manager.to_menu, cell_size)
    
    running = True
    while running:
        
        clock.tick(FPS)
        
        event_handler()
        
        # loads the menu page
        if page_manager.curr_page == 0:
            menu_page.load()
        
        # loads the visualisation page
        elif page_manager.curr_page == 1:
            visualisation_page.load()
        
        else:
            pygame.quit()
            quit()
            
        pygame.display.update()

    pygame.quit()
    quit()


# checks that the main() function is being run from this file (main.py), and not elsewhere
if __name__ == '__main__':

    valid = False
    while not valid:
        
        # get user input
        cell_size = input("Enter size of cells: ")
        
        # presence check
        if cell_size == "":
            print("invalid - try again")
            continue
        
        # type check
        try:
            cell_size = int(cell_size)
        except:
            print("invalid - try again (must be an integer)")
            continue
    
        # range check
        if 5 <= cell_size <= 50:
            valid = True
        else:
            print("invalid - try again (must be between 5 and 50 inclusive)")
    
    main(cell_size)