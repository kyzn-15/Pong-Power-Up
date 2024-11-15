import pygame
import random
import time
from conf import Conf

class PowerUp:
    TYPES = ["speed_boost", "paddle_enlarge", "ball_slow"]
    COOLDOWN_DURATION = Conf.COUNTDOWN

    def __init__(self):
        self.type = random.choice(self.TYPES)
        self.x = random.randint(Conf.WIDTH // 4, Conf.WIDTH * 3 // 4)
        self.y = random.randint(50, Conf.HEIGHT - 50)
        self.radius = 15
        self.active = False
        self.start_time = 0
        self.color = self.get_color()
        self.active_effects = {
            "speed_boost": False,
            "paddle_enlarge": False,
            "ball_slow": False
        }
        self.affected_paddles = []

    def get_color(self):
        colors = {
            "speed_boost": (255, 0, 0),
            "paddle_enlarge": (0, 255, 0),
            "ball_slow": (0, 0, 255)
        }
        return colors[self.type]

    def draw(self, win):
        if not self.active:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        y_offset = 10
        for effect_type, is_active in self.active_effects.items():
            if is_active:
                remaining_time = max(0, self.COOLDOWN_DURATION - (time.time() - self.start_time))
                self.draw_cooldown_indicator(win, effect_type, remaining_time, y_offset)
                y_offset += 30

    def draw_cooldown_indicator(self, win, effect_type, remaining_time, y_offset):
        bar_width = 100
        bar_height = 10
        x = 10
        y = y_offset
        pygame.draw.rect(win, (128, 128, 128), (x, y, bar_width, bar_height))
        progress = remaining_time / self.COOLDOWN_DURATION
        progress_width = int(bar_width * progress)
        pygame.draw.rect(win, self.get_color(), (x, y, progress_width, bar_height))
        font = pygame.font.Font(None, 20)
        text = font.render(effect_type.replace("_", " ").title(), True, (255, 255, 255))
        win.blit(text, (x + bar_width + 10, y))

    def apply_effect(self, paddles, ball):
        if not self.active_effects[self.type]:
            self.active = True
            self.active_effects[self.type] = True
            self.start_time = time.time()
            if self.type == "speed_boost":
                for paddle in paddles:
                    paddle.VEL += 3
            elif self.type == "paddle_enlarge":
                for paddle in paddles:
                    paddle.height += 30
                    self.affected_paddles.append(paddle)
            elif self.type == "ball_slow":
                ball.x_vel = max(1, ball.x_vel - 2)

    def update(self, paddles, ball):
        current_time = time.time()
        for effect_type in self.active_effects:
            if self.active_effects[effect_type]:
                if current_time - self.start_time >= self.COOLDOWN_DURATION:
                    self.remove_effect(effect_type, paddles, ball)
                    self.active_effects[effect_type] = False
                    self.affected_paddles.clear()

    def remove_effect(self, effect_type, paddles, ball):
        if effect_type == "speed_boost":
            for paddle in paddles:
                paddle.VEL -= 3
        elif effect_type == "paddle_enlarge":
            for paddle in self.affected_paddles:
                paddle.height -= 30
        elif effect_type == "ball_slow":
            ball.x_vel = ball.MAX_VEL

    def reset_position(self):
        if not any(self.active_effects.values()):
            self.active = False
            self.type = random.choice(self.TYPES)
            self.x = random.randint(Conf.WIDTH // 4, Conf.WIDTH * 3 // 4)
            self.y = random.randint(50, Conf.HEIGHT - 50)
            self.color = self.get_color()
            self.affected_paddles.clear()
