import cv2
import time
from translate import *
from gamestate import *
from calibration import *
from concurrent_videocapture import ConcurrentVideoCapture
import pygame_gui, pygame

class App:
    def __init__(self, cam_port=0):
            self.cap = ConcurrentVideoCapture(cam_port)
            self.matrix = None
            # Set auto exposure
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # 0.75 to turn on auto exposure

            pygame.init()

            self.window_width = 800
            self.window_height = 600
            self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))

            self.manager = pygame_gui.UIManager((self.window_width, self.window_height),'main.json')
            self.manager.get_theme().load_theme('main.json')
            self.matrix_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 275), (100, 50)),
                                                              text='Matrix',
                                                              manager=self.manager,

                                                              )

            self.transform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 375), (100, 50)),
                                                                 text='Transform',
                                                                 manager=self.manager,

                                                                 )

            self.convert_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 475), (100, 50)),
                                                                 text='Convert',
                                                                 manager=self.manager,

                                                                 )

    def run(self):

        calibration = Calibration(self.manager,self.window_surface)

        running = True
        while running:
            time_delta = time.time()


            grabbed, frame = self.cap.read()
            if not grabbed or frame is None:
                print("Could not read frame")
                continue
            # Convert the color space of the frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame)
            frame_surface = pygame.transform.rotate(frame_surface, -90)
            frame_surface = pygame.transform.scale(frame_surface, (self.window_width/4,self.window_height/4))

            draw_board(self.manager,self.window_surface,self.window_width)
            calibration.draw()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.matrix_button:
                        self.matrix = getMatrix(getChessboardCorners(frame))
                        print("Matrix Successful")
                    if event.ui_element == self.transform_button:
                        translate(frame, self.matrix, "transformed")
                        print("Transform Successful")
                    if event.ui_element == self.convert_button:
                        calibration.update()
                        print("Convert Successful")


                self.manager.process_events(event)
            self.manager.update(time_delta)

            self.window_surface.blit(frame_surface,(self.window_width/2-self.window_width/8,self.window_height-self.window_height/4))
            self.manager.draw_ui(self.window_surface)
            pygame.display.update()

        self.cap.release()
        pygame.quit()

if __name__ == "__main__":
    app = App()
    app.run()
