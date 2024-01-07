import pygame
import pygame_gui

import main
from settings import *
from main import *
class CalibrationWindow:
    def __init__(self):
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height))
        pygame.display.set_caption("Calibration Window")

        # Declaring all the buttons
        self.main_window_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 275), (100, 50)),
                                                               text='Main Window',
                                                               manager=self.manager,
                                                               )

    def show(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.main_window_button:
                        running = False  # Stop updating the current window

                if running:  # Only process events and update the window if running is True
                    self.manager.process_events(event)

                    self.manager.update(0.1)  # Update the UI manager

                    self.window_surface.fill((0, 0, 0))  # Fill the window with black color
                    self.manager.draw_ui(self.window_surface)  # Draw the UI

                    pygame.display.update()  # Update the display

        # When running becomes False, start the main window
        main.start_main()
