import pygame
import pygame_gui
import time
import main
from camera import *
from settings import *
from main import *
from window import *
class CalibrationWindow:
    def __init__(self):
        pygame.init()
        settings.set_value("latest_caption","Calibration Window")
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), settings.return_value("dark_mode"))
        pygame.display.set_caption(settings.return_value("latest_caption"))

        # Declaring all the buttons
        self.main_window_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.window_width/2 + 150, self.window_height - 50), settings.return_value("standard_button")),
                                                               text='Main',
                                                               manager=self.manager,
                                                               )

    def show(self):
        running = True
        clock = pygame.time.Clock()  # Create a clock object
        #windowHandler = WindowHandler()
        settings.set_value("camera_scale",2)
        cameraSurface = camera.return_frame_surface()
        surface_width = cameraSurface.get_width()
        surface_height = cameraSurface.get_height()

        while running:
            time_delta = clock.tick(60) / 1000.0  # Tick the clock and get the time delta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.main_window_button:
                        settings.set_value("camera_scale",4)
                        #windowHandler.switchWindow()
                        running = False  # Stop updating the current window

                if running:  # Only process events and update the window if running is True
                    self.manager.process_events(event)

            self.manager.update(time_delta)  # Update the UI manager as per the time_delta set

            self.window_surface.fill((0, 10, 100))  # Fill the window
            self.manager.draw_ui(self.window_surface)  # Draw the UI

            self.window_surface.blit(camera.return_frame_surface(), (
                (self.window_width - surface_width)/2, (self.window_height - surface_height)/2))

            pygame.display.update()  # Update the display

        # When running becomes False, start the main window
        settings.set_value("latest_caption","Main Window")
        main.start_main()

