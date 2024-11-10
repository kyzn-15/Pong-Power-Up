import pygame
from conf import Conf
import time

class Paddle:
    COLOR = Conf.WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    MAX_VEL = 5
    COLOR = Conf.WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        self.image = pygame.image.load('./assets/ball.png')
        self.angle = 0

    def draw(self, win):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=(self.x, self.y))
        win.blit(rotated_image, new_rect)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.angle += 10

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1
        self.angle = 0

def draw(win, paddles, ball, left_score, right_score):
    win.fill(Conf.BLACK)
    left_score_text = Conf.SCORE_FONT.render(f"{left_score}", 1, Conf.WHITE)
    right_score_text = Conf.SCORE_FONT.render(f"{right_score}", 1, Conf.WHITE)
    win.blit(left_score_text, (Conf.WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (Conf.WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= Conf.HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if left_paddle.y < ball.y < left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                ball.y_vel = ball.MAX_VEL * ((ball.y - (left_paddle.y + left_paddle.height / 2)) / (left_paddle.height / 2))
    else:
        if right_paddle.y < ball.y < right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                ball.y_vel = ball.MAX_VEL * ((ball.y - (right_paddle.y + right_paddle.height / 2)) / (right_paddle.height / 2))

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VEL <= Conf.HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VEL <= Conf.HEIGHT:
        right_paddle.move(up=False)

def countdown(win):
    for i in range(3, 0, -1):
        win.fill(Conf.BLACK)
        countdown_text = Conf.SCORE_FONT.render(str(i), 1, Conf.WHITE)
        win.blit(countdown_text, (Conf.WIDTH // 2 - countdown_text.get_width() // 2, Conf.HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        time.sleep(1)

def main():
    pygame.init()
    WIN = pygame.display.set_mode((Conf.WIDTH, Conf.HEIGHT))
    pygame.display.set_caption("Pong")

    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, Conf.HEIGHT // 2 - Conf.PADDLE_HEIGHT // 2, Conf.PADDLE_WIDTH, Conf.PADDLE_HEIGHT)
    right_paddle = Paddle(Conf.WIDTH - 10 - Conf.PADDLE_WIDTH, Conf.HEIGHT // 2 - Conf.PADDLE_HEIGHT // 2, Conf.PADDLE_WIDTH, Conf.PADDLE_HEIGHT)
    ball = Ball(Conf.WIDTH // 2, Conf.HEIGHT // 2, Conf.BALL_RADIUS)

    left_score = 0
    right_score = 0

    countdown(WIN)

    while run:
        clock.tick(Conf.FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            countdown(WIN)

        elif ball.x > Conf.WIDTH:
            left_score += 1
            ball.reset()
            countdown(WIN)

        won = False
        if left_score >= Conf.WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= Conf.WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = Conf.SCORE_FONT.render(win_text, 1, Conf.WHITE)
            WIN.blit(text, (Conf.WIDTH // 2 - text.get_width() // 2, Conf.HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
            countdown(WIN)

    pygame.quit()

if __name__ == '__main__':
    main()
