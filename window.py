import pygame
import pygame_gui
from settings import *
from main import *
class Window:
    def __init__(self):
        pygame.init()
        settings.set_value("latest_caption", "Window")
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), settings.return_value("dark_mode"))
        pygame.display.set_caption(settings.return_value("latest_caption"))

        # Declaring all the buttons
        self.main_window_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 275), (100, 50)),
                                                               text='Main',
                                                               manager=self.manager,
                                                               )

    def show(self):
        running = True
        clock = pygame.time.Clock()  # Create a clock object
        windowHandler = WindowHandler()
        while running:
            time_delta = clock.tick(60) / 1000.0  # Tick the clock and get the time delta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.main_window_button:
                        windowHandler.switchWindow()
                        running = False  # Stop updating the current window

                if running:  # Only process events and update the window if running is True
                    self.manager.process_events(event)

            self.manager.update(time_delta)  # Update the UI manager as per the time_delta set

            self.window_surface.fill((0, 10, 100))  # Fill the window
            self.manager.draw_ui(self.window_surface)  # Draw the UI

            self.window_surface.blit(camera.return_frame_surface(), (
                self.window_width / 2 - self.window_width / 8, self.window_height - self.window_height / 4))

            pygame.display.update()  # Update the display

        # When running becomes False, start the main window
        settings.set_value("latest_caption", "Main Window")
        main.start_main()

class WindowHandler:
    def switchWindow(self):
        settings.set_value("latest_caption", "Switching Window...")
        pygame.display.set_caption(settings.return_value("latest_caption"))
        pygame.display.update()
        time.sleep(settings.return_value("window_switch_time"))