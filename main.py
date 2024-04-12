import cv2
import time
import gamestate
import pygame_gui
import pygame
import settings
import translate
import window
from calibration import CalibrationWindow
from translate import *
from gamestate import *
from calibration import *
from settingwindow import *
from settings import *
from camera import *
from window import *
old_theme = "dark_mode"
toggle_theme = "dark_mode"
def toggleTheme():
    global toggle_theme
    if toggle_theme == "dark_mode":
        toggle_theme = "light_mode"
    else:
        toggle_theme = "dark_mode"


class App:
    def __init__(self):
        pygame.init()
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))


        self.manager = pygame_gui.UIManager((self.window_width, self.window_height), settings.return_value(toggle_theme))

        self.current_turn = 'white'

        pygame.display.set_caption(settings.return_value("latest_caption"))

        # Declaring all the buttons

        self.play_move_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 - 200, self.window_height - 50), settings.return_value("standard_button")),
            text='Play Move',
            manager=self.manager,

            )
        self.calibration_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 + 100, self.window_height - 50),
                                      settings.return_value("standard_button")),
            text='Calibration',
            manager=self.manager,

            )
        self.setting_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 - 300, self.window_height - 50),
                                      settings.return_value("standard_button")),
            text='Settings',
            manager=self.manager,

        )
        self.white_player = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 0), (self.window_width/4, 100)),
            html_text='<b>White Player Turn</b>',
            manager=self.manager
            )
        self.white_player.text_horiz_alignment = "center"
        self.black_player = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.window_width - self.window_width/4, 0), (self.window_width / 4, 100)),
            html_text='Black Player Turn',
            manager=self.manager
        )

        self.move_history = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.window_width - self.window_width / 4, self.window_height - 300), (self.window_width / 4, 300)),
            html_text='<p><u>Move History</u></p>',
            manager=self.manager
        )

        self.white_player.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        self.black_player.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT)
    def reload_gui(self):
        pygame.init()
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height),
                                            settings.return_value(toggle_theme))
        print(toggle_theme)
        self.play_move_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 - 200, self.window_height - 50),
                                      settings.return_value("standard_button")),
            text='Play Move',
            manager=self.manager,

        )
        self.calibration_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 + 100, self.window_height - 50),
                                      settings.return_value("standard_button")),
            text='Calibration',
            manager=self.manager,

        )
        self.setting_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.window_width / 2 - 300, self.window_height - 50),
                                      settings.return_value("standard_button")),
            text='Settings',
            manager=self.manager,

        )
        self.white_player = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, 0), (self.window_width / 4, 100)),
            html_text='<b>White Player Turn</b>',
            manager=self.manager
        )
        self.white_player.text_horiz_alignment = "center"
        self.black_player = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.window_width - self.window_width / 4, 0), (self.window_width / 4, 100)),
            html_text='Black Player Turn',
            manager=self.manager
        )

        self.move_history = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.window_width - self.window_width / 4, self.window_height - 300),
                                      (self.window_width / 4, 300)),
            html_text='<p><u>Move History</u></p>',
            manager=self.manager
        )

        self.white_player.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
        self.black_player.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT)

    def update_players(self):
        # Update the player text boxes based on the current turn
        if self.current_turn == 'white':
            self.white_player.html_text = '<p><b>White Player Turn</b></p>'
            self.black_player.html_text = '<p>Black Player Turn</p>'
            self.white_player.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
            self.black_player.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT)
        else:
            self.white_player.html_text = '<p>White Player Turn</p>'
            self.black_player.html_text = '<p><b>Black Player Turn</b></p>'
            self.black_player.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
            self.white_player.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_OUT)
        self.white_player.rebuild()
        self.black_player.rebuild()
    def update_move_history(self, moves):
        # Convert the list of moves to a string
        moves_str = '<br>'.join(moves)

        # Update the move history text box
        self.move_history.html_text = f'<p><u>Move History</u></p><br><p>{chessGame.move_list}</p>'
        self.move_history.rebuild()

    def run(self):


        settings.set_value("latest_caption", "Main Window")
        settings.set_value("camera_scale", 8)
        clock = pygame.time.Clock()
        # windowHandler = WindowHandler()
        chessboard = ChessBoard(self.manager, self.window_surface, self.window_width)
        running = True
        chessboard.needUpdateTrue()  # Flag to indicate whether the display needs to be updated

        while running:
            pygame.display.set_caption(settings.return_value("latest_caption"))
            time_delta = clock.tick(60) / 1000.0  # Tick the clock and get the time delta

            cameraSurface = camera.aspect_scale(camera.return_frame_surface(), (300, 200))
            print(toggle_theme)
            global old_theme
            if old_theme == toggle_theme:
                pass
            else:
                old_theme = toggle_theme
                self.reload_gui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    chessboard.needUpdateTrue()  # Set the flag to True when a button is pressed
                    if event.ui_element == self.setting_button:
                        setting_window = SettingWindow()
                        setting_window.show()

                    if event.ui_element == self.play_move_button:
                        translator.translate(camera.return_frame(), translator.returnMatrix(),
                                             translator.return_transformed_image_name())
                        chessGame.movepieces()
                        # Update the turn
                        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                        self.update_players()  # Update the player text boxes

                        settings.set_value("latest_caption", "Main Window")

                    if event.ui_element == self.calibration_button:
                        calibration_window = CalibrationWindow()
                        calibration_window.show()



                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.window_surface.fill((0, 10, 100))  # Fill the window

            if chessboard.needUpdate():  # Only update the display and redraw the chessboard if the flag is True
                chessboard.draw_board(chessGame.get_latest_board_string(),
                                      settings.return_value("chessboard_image_path"))

            self.window_surface.blit(cameraSurface, (
                self.window_width / 2 - cameraSurface.get_width() / 2, self.window_height - cameraSurface.get_height()))

            self.manager.draw_ui(self.window_surface)
            pygame.display.update()
        camera.release_capture()
        pygame.quit()


def start_main():
    if __name__ == "__main__":
        app = App()
        app.run()


start_main()
