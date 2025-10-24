import pygame
import basicUI
import webbrowser
from typing import Callable

pygame.init()

# initialise dimensions and display
width, height = 1000, 500
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# COLOURS
UI_BG_COLOUR = (50, 50, 50)
UI_BUTTON_COLOUR = (60, 60, 60)
UI_TEXT_COLOUR = (100, 100, 100)

def draw_menu(buttons) -> None:
    
    # fill the screen with the background colour, draw the buttons, and update the display
    win.fill(UI_BG_COLOUR)
    
    for button in buttons:
        button.draw()
    
    pygame.display.update()

def quit_func() -> None:
    # function to quit the program
    
    pygame.quit()
    quit()

def docs_func() -> None:
    # function to open the documentation page (on google docs)
    
    webbrowser.open("https://docs.google.com/document/d/1U96vEvA0jDv8XYHGnGShQUluY2gDUlA39RXWsx02tb4/edit")

def menu(width: int, height: int, main_func: Callable) -> None:
    
    # initialise the margin (gap between buttons for usability), and create an empty list for buttons
    margin = 5
    menu_buttons = []
    
    # create buttons to open the visualisation section of the program (START), quit the program, and open documentation
    # originally sets the button position to (0, 0), and then readjusts it (via .center) to center it on the menu page
    # appends the button to the menu_buttons variable to access all buttons more efficiently
    
    start_button = basicUI.Button(win, "START", main_func, (0, 0), fontsize=60,
                                  fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    start_button.center = (width // 2, height // 2 - start_button.button_rect.height // 2 - margin)
    menu_buttons.append(start_button)
    
    quit_button = basicUI.Button(win, "QUIT", quit_func, (0, 0), fontsize=60,
                                 fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    quit_button.center = (width // 2, height // 2 + quit_button.button_rect.height // 2 + margin)
    menu_buttons.append(quit_button)
    
    docs_button = basicUI.Button(win, "DOCS", docs_func, (0, 0), fontsize=20,
                                 fg=UI_TEXT_COLOUR, bg=UI_BUTTON_COLOUR)
    docs_button.center = (width - docs_button.button_rect.width // 2 - margin*2,
                          docs_button.button_rect.height // 2 + margin*2)
    menu_buttons.append(docs_button)
    
    running = True
    
    while running:
        
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for button in menu_buttons:
            button.update()
            
        draw_menu(menu_buttons)
    
    pygame.quit()
    quit()

def draw_main() -> None:
    
    # Fill the screen with the background colour and update the display
    win.fill(UI_BG_COLOUR)
    pygame.display.update()

def main() -> None:
    
    running = True
    
    while running:
    
        # ensures that the program cannot be run at more than 60 fps
        clock.tick(60)
        
        # check if user wants to quit the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        draw_main()

    # if program is no longer running, quit
    pygame.quit()
    quit()

# only runs the main file if it is being run from main.py
if __name__ == '__main__':
    
    menu(width, height, main)
    
