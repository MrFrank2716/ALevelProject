import cv2
import time
import gamestate
import pygame_gui
import pygame
import settings
import window
from translate import *
from gamestate import *
from calibration import *
from settings import *
from camera import *
from window import *

class App:
    def __init__(self):
        pygame.init()

        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), settings.return_value("dark_mode"))

        pygame.display.set_caption(settings.return_value("latest_caption"))

        # Declaring all the buttons
        self.matrix_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 275), settings.return_value("standard_button")),
                                                          text='Matrix',
                                                          manager=self.manager,

                                                          )

        self.transform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 375), settings.return_value("standard_button")),
                                                             text='Transform',
                                                             manager=self.manager,

                                                             )

        self.convert_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 475), settings.return_value("standard_button")),
                                                           text='Convert',
                                                           manager=self.manager,

                                                           )
        self.calibration_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.window_width/2 + 100, self.window_height-50), settings.return_value("standard_button")),
                                                               text='Calibration',
                                                               manager=self.manager,

                                                               )

    def run(self):
        settings.set_value("latest_caption","Main Window")
        settings.set_value("camera_scale",8)
        clock = pygame.time.Clock()
        #windowHandler = WindowHandler()
        chessboard = ChessBoard(self.manager, self.window_surface, self.window_width)
        running = True
        chessboard.needUpdateTrue()  # Flag to indicate whether the display needs to be updated


        while running:
            pygame.display.set_caption(settings.return_value("latest_caption"))
            time_delta = clock.tick(60) / 1000.0  # Tick the clock and get the time delta

            cameraSurface = camera.aspect_scale(camera.return_frame_surface(),(300,200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    chessboard.needUpdateTrue() # Set the flag to True when a button is pressed
                    if event.ui_element == self.matrix_button:
                        translator.setMatrix(
                            translator.calculateMatrix(translator.getChessboardCorners(camera.return_frame())))
                        time.sleep(0.27)
                        settings.set_value("latest_caption","Main Window")

                    if event.ui_element == self.transform_button:
                        translator.translate(camera.return_frame(), translator.returnMatrix(),
                                             translator.return_transformed_image_name())
                        time.sleep(0.27)
                        settings.set_value("latest_caption","Main Window")

                    if event.ui_element == self.convert_button:
                        gamestate.movepieces(game.board)
                        time.sleep(0.27)
                        settings.set_value("latest_caption","Main Window")

                    if event.ui_element == self.calibration_button:
                        #windowHandler.switchWindow()
                        calibration_window = CalibrationWindow()
                        calibration_window.show()


                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.window_surface.fill((0, 10, 100))  # Fill the window

            if chessboard.needUpdate():  # Only update the display and redraw the chessboard if the flag is True
                chessboard.draw_board(game.get_latest_board_string(), settings.return_value("chessboard_image_path"))

            self.window_surface.blit(cameraSurface, (
                self.window_width / 2 - cameraSurface.get_width()/2, self.window_height - cameraSurface.get_height()))

            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
        camera.release_capture()
        pygame.quit()


def start_main():
    if __name__ == "__main__":
        app = App()
        app.run()


start_main()
