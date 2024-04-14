import pygame
import pygame_gui
import main
from settings import *
from main import *
from camera import *
class cameraSettings:
    def __init__(self):
        pygame.init()
        settings.set_value("latest_caption", "Camera Settings")
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height),
                                            settings.return_value(main.toggle_theme))
        pygame.display.set_caption(settings.return_value("latest_caption"))
        self.buttons = {}  # This line to initialize the buttons dictionary
        self.button_width = self.window_width // 4
        self.button_height = self.window_height // 3
        self.labels = ["Back to Settings", "Frame Rate", "Colour Space", "" , "60" , "RGB"]
        self.label_index = 0
        self.frame_rates = ["10", "20", "30", "60", "120"]
        self.frame_rate_index = self.frame_rates.index(str(settings.return_value("fps")))  # Start at 60 FPS
        self.frame_rate_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((2 * self.button_width, 3 * self.button_height),
                                              (self.button_width, self.button_height)),
                    text=self.frame_rates[self.frame_rate_index],
                    manager=self.manager)
        self.colour_spaces = ["RGB", "HSV", "Gray", "YCrCb"]
        self.colour_spaces_index = self.colour_spaces.index(str(settings.return_value("colourSpace")))
        self.colour_spaces_button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((2 * self.button_width, 3 * self.button_height),
                                              (self.button_width, self.button_height)),
                    text=self.colour_spaces[self.colour_spaces_index],
                    manager=self.manager)
        self.camera_port = 0


        for i in range(2):
            for j in range(3):
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((i * self.button_width, j * self.button_height),
                                              (self.button_width, self.button_height)),
                    text=self.labels[self.label_index],
                    manager=self.manager)
                self.buttons[self.labels[self.label_index]] = button  # This line to store the button in the dictionary
                # If this is the frame rate button, store it separately
                if self.labels[self.label_index] == str(settings.return_value("fps")):
                    self.frame_rate_button = button
                if self.labels[self.label_index] == str(settings.return_value("colourSpace")):
                    self.colour_spaces_button = button
                self.label_index += 1
                self.colour_spaces_index += 1

    def show(self):
        running = True
        clock = pygame.time.Clock()  # Create a clock object
        settings.set_value("camera_scale", 4)
        windowHandler = WindowHandler()
        while running:
            time_delta = clock.tick(settings.return_value("fps")) / 1000.0  # Tick the clock and get the time delta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.buttons["Back to Settings"]:
                        windowHandler.switchWindow()
                        running = False  # Stop updating the current window
                    if event.ui_element == self.buttons["Frame Rate"]:
                        # Update the frame rate index and loop back to 0 if it's out of range
                        self.frame_rate_index = (self.frame_rate_index + 1) % len(self.frame_rates)
                        # Update the label of the frame rate button with the new frame rate
                        self.frame_rate_button.set_text(str(self.frame_rates[self.frame_rate_index]))
                        settings.set_value("fps", int(self.frame_rates[self.frame_rate_index]))

                    if event.ui_element == self.buttons["Colour Space"]:
                        # Update the frame rate index and loop back to 0 if it's out of range
                        self.colour_spaces_index = (self.colour_spaces_index + 1) % len(self.colour_spaces)
                        # Update the label of the frame rate button with the new frame rate
                        self.colour_spaces_button.set_text(str(self.colour_spaces[self.colour_spaces_index]))
                        settings.set_value("colourSpace", str(self.colour_spaces[self.colour_spaces_index]))

                if running:  # Only process events and update the window if running is True
                    self.manager.process_events(event)

            self.manager.update(time_delta)  # Update the UI manager as per the time_delta set

            self.window_surface.fill((0, 10, 100))  # Fill the window
            self.manager.draw_ui(self.window_surface)  # Draw the UI

            cameraSurface = pygame.transform.rotate(camera.return_frame_surface(),
                                                    90)
            cameraSurface = camera.aspect_scale(cameraSurface, (650, 500))
            surface_width = cameraSurface.get_width()
            surface_height = cameraSurface.get_height()

            self.window_surface.blit(cameraSurface, (
                self.window_width / 2 - surface_width / 2 + 200, self.window_height / 2 - surface_height / 2))

            pygame.display.update()  # Update the display

        # When running becomes False, start the main window
        settings.set_value("latest_caption", "Main Window")
        main.start_main()

class WindowHandler:
    def switchWindow(self):
        settings.set_value("latest_caption", "Switching Window...")
        pygame.display.set_caption(settings.return_value("latest_caption"))
        pygame.display.update()