from concurrent_videocapture import ConcurrentVideoCapture
import cv2
import pygame
from settings import *


class Camera:

    def __init__(self, cam_port=0):
        self.cap = ConcurrentVideoCapture(cam_port)
        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)  # 0.75 to turn on auto exposure
        self.frame = None
        self.window_width = settings.return_value("window_width")
        self.window_height = settings.return_value("window_height")

    def return_frame_surface(self):
        grabbed, frame = self.cap.read()
        if not grabbed or frame is None:
            print("Could not read frame")
        # Convert the color space of the frame
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(self.frame)
        frame_surface = pygame.transform.rotate(frame_surface, -90)

        # Get the minimum dimension of the frame
        width = frame_surface.get_width()
        height = frame_surface.get_height()

        # Scale the surface to a 1:1 aspect ratio
        frame_surface = pygame.transform.scale(frame_surface, (
        width / settings.return_value("camera_scale"), height / settings.return_value("camera_scale")))
        return frame_surface

    def return_frame(self):
        return self.frame

    def release_capture(self):
        self.cap.release()


camera = Camera()
