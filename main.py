import cv2
import time
from translate import *
from concurrent_videocapture import ConcurrentVideoCapture
import pygame_gui, pygame

class App:
    def __init__(self, cam_port=0):
        self.cap = ConcurrentVideoCapture(cam_port)
        self.matrix = None

        pygame.init()

        self.window_width = 800
        self.window_height = 600
        self.window_surface = pygame.display.set_mode((self.window_width, self.window_height))

        self.manager = pygame_gui.UIManager((self.window_width, self.window_height))

        self.matrix_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                          text='Matrix',
                                                          manager=self.manager)

        self.transform_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 375), (100, 50)),
                                                             text='Transform',
                                                             manager=self.manager)

    def run(self):
        running = True
        while running:
            init = time.time()
            time_delta = init
            grabbed, frame = self.cap.read()
            if not grabbed or frame is None:
                print("Could not read frame")
                continue
            frame_surface = pygame.surfarray.make_surface(frame)
            frame_surface = pygame.transform.rotate(frame_surface, -90)
            frame_surface = pygame.transform.scale(frame_surface, (self.window_width/4,self.window_height/4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.matrix_button:
                        print("Matrix Successful")
                        self.matrix = getMatrix(getChessboardCorners(frame))
                    if event.ui_element == self.transform_button:
                        print("Transform Successful")
                        translate(frame, self.matrix, "transformed")

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
