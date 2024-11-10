import pygame
import random
from conf import Conf

class PowerUp:
    TYPES = ["speed_boost", "paddle_enlarge", "ball_slow"]

    def __init__(self):
        self.type = random.choice(self.TYPES)
        self.x = random.randint(Conf.WIDTH // 4, Conf.WIDTH * 3 // 4)
        self.y = random.randint(50, Conf.HEIGHT - 50)
        self.radius = 15
        self.color = (255, 0, 0) if self.type == "speed_boost" else (0, 255, 0) if self.type == "paddle_enlarge" else (0, 0, 255)
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
    
    def apply_effect(self, paddle, ball):
        if self.type == "speed_boost":
            paddle.VEL += 3  
        elif self.type == "paddle_enlarge":
            paddle.height += 30  
        elif self.type == "ball_slow":
            ball.x_vel = max(1, ball.x_vel - 2) 
