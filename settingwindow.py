import pygame
from serial.tools import list_ports
import pygame_gui
import main
from settings import *
from calibration import CalibrationWindow
from main import *
from camera import *
class SettingWindow:
    def __init__(self):
        pygame.init()
        settings.set_value("latest_caption", "Window")
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height))
        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), settings.return_value(main.toggle_theme))
        pygame.display.set_caption(settings.return_value("latest_caption"))
        self.buttons = {}  # This line to initialize the buttons dictionary
        labels = ["Back to Main","Toggle Theme","Camera Settings","Calibration Window","Camera Selected","Game Settings"]
        label_index = 0
        self.camera_port = 0
        self.button_width = self.window_width // 4
        self.button_height = self.window_height // 3

        for i in range(2):
            for j in range(3):
                button = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((i * self.button_width, j * self.button_height), (self.button_width, self.button_height)),
                    text=labels[label_index],
                    manager=self.manager)
                self.buttons[labels[label_index]] = button  # This line to store the button in the dictionary
                label_index += 1

        self.selected_camera = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.button_width, self.button_height), (self.window_width / 4 , 50)),
            html_text='Camera 1',
            manager=self.manager
        )
        self.selected_camera.text_horiz_alignment = "center"
    def toggleTheme(self):
        toggle_theme = main.toggle_theme
        if toggle_theme == "dark_mode":
            main.toggle_theme = "light_mode"
        else:
            main.toggle_theme = "dark_mode"
        self.__init__()

    def show(self):
        running = True
        clock = pygame.time.Clock()  # Create a clock object
        settings.set_value("camera_scale", 4)
        windowHandler = WindowHandler()
        while running:
            time_delta = clock.tick(60) / 1000.0  # Tick the clock and get the time delta
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.buttons["Back to Main"]:
                        windowHandler.switchWindow()
                        running = False  # Stop updating the current window
                    if event.ui_element == self.buttons["Calibration Window"]:
                        windowHandler.switchWindow()
                        calibration_window = CalibrationWindow()
                        calibration_window.show()
                        running = False  # Stop updating the current window
                    if event.ui_element == self.buttons["Camera Selected"]:
                        if self.camera_port == 0:
                            camera.switch_camera(1)
                            self.camera_port = 1
                            self.selected_camera.text_horiz_alignment = "center"
                            self.selected_camera.set_text("Camera 2")
                        else:
                            camera.switch_camera(0)
                            self.camera_port = 0
                            self.selected_camera.set_text("Camera 1")
                    if event.ui_element == self.buttons["Toggle Theme"]:
                        #self.toggleTheme()
                        main.toggleTheme()
                        self.__init__()
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
