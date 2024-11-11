import pygame

pygame.init()
pygame.font.init()

class Conf:
    WIDTH, HEIGHT = 900, 700
    FPS = 120

    WHITE = (255, 255, 255)
    BLACK = (28, 117, 28)

    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    BALL_RADIUS = 20

    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WINNING_SCORE = 5

    PADDLE_COLOR = WHITE
    PADDLE_VEL = 4
    BALL_COLOR = WHITE
    BALL_MAX_VEL = 5

    COUNTDOWN = 3
