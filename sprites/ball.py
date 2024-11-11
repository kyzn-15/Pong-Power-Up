import pygame
from conf import Conf

class Ball:
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        self.image = pygame.image.load("./assets/ball.png")
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        self.angle = 0

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        win.blit(rotated_image, new_rect.topleft)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.angle = (self.angle + 5) % 360

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        self.angle = 0
