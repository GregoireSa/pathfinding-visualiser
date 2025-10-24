"""
A module containing utility classes for creating text elements, buttons, and dropdowns in Pygame.

This module provides functionality for creating text elements, buttons, and dropdowns in a Pygame application.
These elements can be used for user interaction and interface design.

Functions:
    text(surface: pygame.Surface, info_text: str, pos: tuple, colour: tuple=(0, 0, 0),
         size: int=30, pos_type: str='center') -> None:
        Creates a text element on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
            info_text (str): The text to display.
            pos (tuple): The position of the text element.
            colour (tuple): The color of the text. Default is black (0, 0, 0).
            size (int): The font size of the text. Default is 30.
            pos_type (str): The position type of the text element. Default is 'center'.

Classes:
    Button:
        Represents a clickable button element.

        Methods:
            __init__(surface: pygame.Surface, button_text: str, command: Callable, pos: tuple,
                     fontsize: int=30, fg: tuple=(0, 0, 0), bg: tuple=(255, 255, 255)) -> None:
                Initializes a new Button object.
            change_text(new_text: str) -> None:
                Changes the text displayed on the button.
            update() -> None:
                Checks for interactions with the button and updates its state.
            draw() -> None:
                Draws the button on the surface.

    Dropdown:
        Represents a dropdown menu element.

        Methods:
            __init__(surface: pygame.Surface, default_text: str, pos: tuple,
                     fontsize: int=30, fg: tuple=(0, 0, 0), bg: tuple=(255, 255, 255),
                     pad_x: int=30, pad_y: int=20) -> None:
                Initializes a new Dropdown object.
            add_option(option_text: str, command: Callable) -> None:
                Adds an option to the dropdown menu.
            update() -> None:
                Checks for interactions with the dropdown menu and updates its state.

Private Classes:
    _DropdownOption:
        Represents an option in a dropdown menu.

        Methods:
            __init__(box_rect: pygame.Rect, text_rect: pygame.Rect, option_text: str, command: Callable) -> None:
                Initializes a new _DropdownOption object.
"""

import pygame
from typing import Callable

pygame.init()


def text(surface: pygame.Surface, info_text: str, pos: tuple,
         colour: tuple=(0, 0, 0), size: int=30, pos_type: str='center') -> None:
    """
    Creates a text element on the given surface.

    Args:
        surface (pygame.Surface): The surface to draw the text on.
        info_text (str): The text to be displayed.
        pos (tuple): The position of the text on the surface.
        colour (tuple): The color of the text. Default is black (0, 0, 0).
        size (int): The font size of the text. Default is 30.
        pos_type (str): The type of position specified. Default is 'center'.
            Options: 'center', 'topleft'.
    """
    
    # create a font and text using pygame
    text_font = pygame.font.Font(None, size)
    info = text_font.render(info_text, True, colour)
    # check if the user wants to set the position as the center or top left of the text block
    if pos_type == 'center':
        text_rect = info.get_rect(center=pos)
    elif pos_type == 'topleft':
        text_rect = info.get_rect(topleft=pos)
    # draw the text onto the surface
    surface.blit(info, text_rect)


class Button:
    """
    Represents a clickable button element.

    Attributes:
        surface (pygame.Surface): The surface to draw the button on.
        command (Callable): The function to execute when the button is clicked.
        pos (tuple): The position of the button on the surface.
        fontsize (int): The font size of the button text. Default is 30.
        fg (tuple): The foreground color of the button text. Default is black (0, 0, 0).
        bg (tuple): The background color of the button. Default is white (255, 255, 255).

    Methods:
        change_text(new_text: str) -> None:
            Changes the text displayed on the button.
        update() -> None:
            Checks for interactions with the button and updates its state.
        draw() -> None:
            Draws the button on the surface.
    """
    
    def __init__(self, surface: pygame.Surface, button_text: str, command: Callable, pos: tuple,
                 fontsize: int=30, fg: tuple=(0, 0, 0), bg: tuple=(255, 255, 255)) -> None:
        
        self.surface = surface
        self.command = command
        self.pos = pos
        self.fg, self.bg = fg, bg
        self.click_state = False
        
        self.text = button_text
        self.fontsize = fontsize
        self.font = pygame.font.Font(None, self.fontsize)
        self.info = self.font.render(self.text, True, self.fg)

        # initialise pygame Rect objects for both the text and the button surrounding the text
        self.info_rect = self.info.get_rect(topleft=self.pos)
        self.button_rect = self.info_rect.inflate(20, 20)
        self.center = self.button_rect.center
        self.info_rect.center = self.center

    def change_text(self, new_text: str) -> None:
        """Method to update/change the text on the button"""
        
        self.text = new_text
        self.info = self.font.render(self.text, True, self.fg)

    def update(self) -> None:
        """Method to check interactions with the button"""

        self.button_rect.center = self.center
        self.info_rect.center = self.center

        # get the mouse position and check whether the mouse has been pressed/the mouse is on the button
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not self.click_state:
            # run the command and set click state to true to stop the command from running repeatedly
            self.click_state = True
            self.command()
        if not pygame.mouse.get_pressed()[0] and self.click_state:
            # reset the click state to false if the mouse is not being pressed
            self.click_state = False

    def draw(self) -> None:
        """draw all aspects of the button onto the surface (text, button, and border)"""

        pygame.draw.rect(self.surface, self.bg, self.button_rect)
        pygame.draw.rect(self.surface, self.fg, self.button_rect, width=2)
        self.surface.blit(self.info, self.info_rect)


class _DropdownOption:
    """
    Represents an option in a dropdown menu.

    Attributes:
        box_rect (pygame.Rect): The bounding box of the option.
        text_rect (pygame.Rect): The bounding box of the option text.
        text (pygame.Surface): The text displayed for the option.
        command (Callable): The function to execute when the option is selected.
    """
    
    def __init__(self, box_rect: pygame.Rect, text_rect: pygame.Rect, option_text: str, command: Callable) -> None:
        
        self.box_rect = box_rect
        self.text_rect = text_rect
        self.text = option_text
        self.command = command


class Dropdown:
    """
    Represents a dropdown menu element.

    Attributes:
        surface (pygame.Surface): The surface to draw the dropdown on.
        default_text (str): The default text displayed in the dropdown.
        pos (tuple): The position of the dropdown on the surface.
        fontsize (int): The font size of the dropdown text. Default is 30.
        fg (tuple): The foreground color of the dropdown text. Default is black (0, 0, 0).
        bg (tuple): The background color of the dropdown. Default is white (255, 255, 255).
        pad_x (int): The padding in the x-direction. Default is 30.
        pad_y (int): The padding in the y-direction. Default is 20.

    Methods:
        add_option(option_text: str, command: Callable) -> None:
            Adds an option to the dropdown menu.
        update() -> None:
            Checks for interactions with the dropdown menu and updates its state.
    """

    def __init__(self, surface: pygame.Surface, default_text: str, pos: tuple,
                 fontsize: int=30, fg: tuple=(0, 0, 0), bg: tuple=(255, 255, 255),
                 pad_x: int=30, pad_y: int=20) -> None:

        self.surface = surface
        self.pos = pos
        self.fg, self.bg = fg, bg
        self.state = False
        self.click_state = False

        self.text = default_text
        self.fontsize = fontsize
        self.font = pygame.font.Font(None, self.fontsize)
        self.pad_x, self.pad_y = pad_x, pad_y
        self.border_width = 2

        self.bar_text = self.font.render(self.text, True, self.fg)
        self.bar_text_rect = self.bar_text.get_rect(topleft=self.pos)
        self.bar_box_rect = self.bar_text_rect.inflate(self.pad_x, self.pad_y)
        self.bar_text_rect.center = self.bar_box_rect.center

        self.drop_text = self.font.render('v', True, self.fg)
        self.drop_pos = (self.bar_box_rect.topright[0] + (self.pad_x // 2) - self.border_width,
                         self.bar_box_rect.topright[1] + (self.pad_y // 2))
        self.drop_text_rect = self.drop_text.get_rect(topleft=self.drop_pos)
        self.drop_box_rect = self.drop_text_rect.inflate(self.pad_x, self.pad_y)

        self.options = []
        self.option_boxes = []
        self.options_height = 0

    def add_option(self, option_text: str, command: Callable) -> None:

        self.options.append((option_text, command))

        if len(self.options) == 1:
            text_pos = (self.bar_box_rect.bottomleft[0],
                        self.bar_box_rect.bottomleft[1] - self.border_width)
            self.bar_text = self.font.render(option_text, True, self.fg)
        else:
            text_pos = (self.option_boxes[-1].box_rect.bottomleft[0],
                        self.option_boxes[-1].box_rect.bottomleft[1] - self.border_width)

        info = self.font.render(option_text, True, self.fg)
        info_text_rect = info.get_rect(topleft=(0, 0))
        info_box_rect = info_text_rect.inflate(self.pad_x, self.pad_y)
        info_box_rect.topleft = text_pos
        info_box_rect.width = self.bar_box_rect.width
        info_text_rect.center = info_box_rect.center

        self.option_boxes.append(_DropdownOption(info_box_rect, info_text_rect, info, command))
        self.options_height += self.fontsize

    def update(self) -> None:
        """Method to check interactions with the dropdown"""

        mouse_pos = pygame.mouse.get_pos()

        if self.drop_box_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and self.click_state is False:

            # checks if the dropdown is open or closed
            self.click_state = True

            if self.state is False:
                self.drop_text = self.font.render("^", True, self.fg)
                self.state = True
            elif self.state is True:
                self.drop_text = self.font.render("v", True, self.fg)
                self.state = False

        # resets the click state to False if the mouse is not pressed
        if not pygame.mouse.get_pressed()[0] and self.click_state is True:
            self.click_state = False

        # draws the dropdown
        pygame.draw.rect(self.surface, self.bg, self.bar_box_rect)
        pygame.draw.rect(self.surface, self.fg, self.bar_box_rect, width=self.border_width)
        self.bar_text_rect.center = self.bar_box_rect.center
        self.surface.blit(self.bar_text, self.bar_text_rect)

        pygame.draw.rect(self.surface, self.bg, self.drop_box_rect)
        pygame.draw.rect(self.surface, self.fg, self.drop_box_rect, width=self.border_width)
        self.surface.blit(self.drop_text, self.drop_text_rect)
        
        # if the dropdown is open and there are options to display
        if self.state is True and self.options:
            
            # draw boxes and check for interactions
            for box in self.option_boxes:

                if box.box_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and self.click_state is False:

                    self.click_state = True
                    box.command()

                    self.drop_text = self.font.render("v", True, self.fg)
                    self.bar_text = box.text
                    self.state = False

                if not pygame.mouse.get_pressed()[0] and self.click_state is True:
                    self.click_state = False

                if self.state is True:
                    pygame.draw.rect(self.surface, self.bg, box.box_rect)
                    pygame.draw.rect(self.surface, self.fg, box.box_rect, width=self.border_width)
                    self.surface.blit(box.text, box.text_rect)