import pygame
import pygame_gui
import time
import json
import main
from camera import *
from settings import *
from main import *
from window import *
with open('calibration.json') as json_file:
    button_colours = json.load(json_file)

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
        self.main_window_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.window_width/2 + 100, self.window_height - 50), settings.return_value("standard_button")),
                                                               text='Main',
                                                               manager=self.manager,
                                                               )

        self.rotate_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 , self.window_height - 50),
                                      settings.return_value("standard_button")),
            text='Rotate',
            manager=self.manager,
            )

        self.top_left_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 - 350, 50),
                                      settings.return_value("calibration_button")),
            text='Top Left (A8)',
            manager=self.manager,
            object_id='#calibration_button'
            )

        self.top_right_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 + 190, 50),
                                      settings.return_value("calibration_button")),
            text='Top Right (H8)',
            manager=self.manager,
            object_id='#calibration_button'
        )

        self.bottom_left_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 - 350, self.window_height - 100),
                                      settings.return_value("calibration_button")),
            text='Bottom Left (A1)',
            manager=self.manager,
            object_id='#calibration_button'
        )

        self.bottom_right_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 + 190, self.window_height - 100),
                                      settings.return_value("calibration_button")),
            text='Bottom Right (H1)',
            manager=self.manager,
            object_id='#calibration_button'
        )

        self.matrix_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 - 200, self.window_height - 50), (200, 50)),
            text='Capture Matrix',
            manager=self.manager,

        )

    def show(self):
        running = True
        clock = pygame.time.Clock()  # Create a clock object
        #windowHandler = WindowHandler()
        settings.set_value("camera_scale",2)
        #cameraSurface = camera.return_frame_surface()


        while running:
            time_delta = clock.tick(60) / 1000.0  # Tick the clock and get the time delta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.main_window_button:
                        settings.set_value("camera_scale",4)
                        running = False  # Stop updating the current window

                    if event.ui_element == self.rotate_button:
                        angle = settings.return_value("calibration_angle") + 90
                        settings.set_value("calibration_angle", angle)

                    if event.ui_element == self.matrix_button:
                        translator.setMatrix(
                            translator.calculateMatrix(translator.getChessboardCorners(camera.return_frame())))

                        settings.set_value("latest_caption", "Main Window")

                if running:  # Only process events and update the window if running is True
                    self.manager.process_events(event)

            self.manager.update(time_delta)  # Update the UI manager as per the time_delta set

            self.window_surface.fill((0, 10, 100))  # Fill the window

            cameraSurface = pygame.transform.rotate(camera.return_frame_surface(), settings.return_value("calibration_angle"))
            cameraSurface = camera.aspect_scale(cameraSurface,(650, 500))
            surface_width = cameraSurface.get_width()
            surface_height = cameraSurface.get_height()

            self.window_surface.blit(cameraSurface, (
                self.window_width / 2 - surface_width /2, self.window_height /2 - surface_height /2))

            self.manager.draw_ui(self.window_surface)  # Draw the UI

            pygame.display.update()  # Update the display

        # When running becomes False, start the main window
        settings.set_value("latest_caption","Main Window")
        settings.set_value("camera_scale", 8)
        main.start_main()

