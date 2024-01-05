import pygame
import pygame_gui

class Calibration:
    def __init__(self, manager, surface):
        self.manager = manager
        self.surface = surface
        self.font = pygame.font.Font(None, 24)
        self.text_a1 = self.font.render('A1', True, (0, 0, 0))
        self.text_h8 = self.font.render('H8', True, (0, 0, 0))
        self.angle = 90

    def draw(self):
        rotated_a1 = pygame.transform.rotate(self.text_a1, self.angle)
        rotated_h8 = pygame.transform.rotate(self.text_h8, self.angle)

        rect_a1 = rotated_a1.get_rect(center=(100, 500))  # bottom left
        rect_h8 = rotated_h8.get_rect(center=(700, 100))  # top right

        self.surface.blit(rotated_a1, rect_a1)
        self.surface.blit(rotated_h8, rect_h8)

    def update(self):
        self.angle = (self.angle + 90) % 360  # rotate by 90 degree
