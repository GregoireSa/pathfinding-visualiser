import pygame
import webbrowser
from typing import Callable

# import necessary project files
import basicUI
import colours

pygame.init()


class Menu:
    """
    Represents the main menu page of the application.

    This class provides functionality for displaying the main menu, including a key for cell types
    and buttons for starting the application, quitting the program, and accessing documentation.

    Attributes:
        surface (pygame.Surface): The surface to draw on.
        width (int): The width of the menu.
        height (int): The height of the menu.
        main_func (Callable): The function to call when starting the application.

    Methods:
        load() -> None:
            Draws the main menu page and handles interactions with buttons.
        quit_func() -> None:
            Closes the program.
        docs_func() -> None:
            Opens the documentation page in a new tab.
    """
    
    def __init__(self, surface: pygame.Surface, width: int, height: int, main_func: Callable) -> None:

        self.surface = surface
        self.width, self.height = width, height
        self.main_func = main_func
        self.margin = 5

        self.key_fontsize = 30
        self.key_x, self.key_y = 30, 30
        self.key_text = [
            "Key:",
            "- Start => green",
            "- Finish => red",
            "- Searched => black",
            "- Searching => turquoise",
            "- Path => purple"
        ]

        self.buttons = []

        self.start_button = basicUI.Button(self.surface, "START", main_func, (0, 0), fontsize=60,
                                           fg=colours.UI_TEXT_COLOUR, bg=colours.UI_BUTTON_COLOUR)
        self.start_button.center = (width // 2, height // 2 - self.start_button.button_rect.height // 2 - self.margin)
        self.buttons.append(self.start_button)

        self.quit_button = basicUI.Button(self.surface, "QUIT", self.quit_func, (0, 0), fontsize=60,
                                          fg=colours.UI_TEXT_COLOUR, bg=colours.UI_BUTTON_COLOUR)
        self.quit_button.center = (width // 2, height // 2 + self.start_button.button_rect.height // 2 + self.margin)
        self.buttons.append(self.quit_button)

        self.docs_button = basicUI.Button(self.surface, "DOCS", self.docs_func, (0, 0), fontsize=20,
                                          fg=colours.UI_TEXT_COLOUR, bg=colours.UI_BUTTON_COLOUR)
        self.docs_button.center = (width - self.docs_button.button_rect.width // 2 - self.margin*2,
                                   self.docs_button.button_rect.height // 2 + self.margin*2)
        self.buttons.append(self.docs_button)

    def load(self) -> None:
        """ Draws the main menu page and checks interactions with buttons """
        
        self.surface.fill(colours.UI_BG_COLOUR)

        for button in self.buttons:

            button.update()
            button.draw()
        
        for i, line in enumerate(self.key_text):
            basicUI.text(self.surface, line, (self.key_x, self.key_y + (self.key_fontsize * i)),
                         colours.UI_TEXT_COLOUR, pos_type='topleft')

    @ staticmethod
    def quit_func() -> None:
        """ Closes the program """
        
        pygame.quit()
        quit()

    @ staticmethod
    def docs_func() -> None:
        """ Opens the coursework documentation page in a new tab """
        
        webbrowser.open("https://docs.google.com/document/d/1U96vEvA0jDv8XYHGnGShQUluY2gDUlA39RXWsx02tb4/edit")
