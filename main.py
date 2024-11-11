import pygame
import random
import time
from conf import Conf
from sprites.paddle import Paddle
from sprites.ball import Ball
from sprites.power_up import PowerUp

pygame.init()

WIN = pygame.display.set_mode((Conf.WIDTH, Conf.HEIGHT))
pygame.display.set_caption("Pong")

def draw(win, paddles, ball, left_score, right_score, power_up):
    win.fill(Conf.BLACK)
    left_score_text = Conf.SCORE_FONT.render(f"{left_score}", 1, Conf.WHITE)
    right_score_text = Conf.SCORE_FONT.render(f"{right_score}", 1, Conf.WHITE)
    win.blit(left_score_text, (Conf.WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (Conf.WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    for i in range(10, Conf.HEIGHT, Conf.HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, Conf.WHITE, (Conf.WIDTH // 2 - 5, i, 10, Conf.HEIGHT // 20))
    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)
    power_up.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= Conf.HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                ball.y_vel = -1 * (difference_in_y / reduction_factor)
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                ball.y_vel = -1 * (difference_in_y / reduction_factor)

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= Conf.HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= Conf.HEIGHT:
        right_paddle.move(up=False)

def countdown(win):
    for i in range(3, 0, -1):
        win.fill(Conf.BLACK)
        countdown_text = Conf.SCORE_FONT.render(str(i), 1, Conf.WHITE)
        win.blit(countdown_text, (Conf.WIDTH // 2 - countdown_text.get_width() // 2,
                                  Conf.HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        time.sleep(1)

def show_winner(win, winner_text):
    win.fill(Conf.BLACK)
    text = Conf.SCORE_FONT.render(winner_text, 1, Conf.WHITE)
    win.blit(text, (Conf.WIDTH // 2 - text.get_width() // 2, Conf.HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, Conf.HEIGHT // 2 - Conf.PADDLE_HEIGHT // 2,
                         Conf.PADDLE_WIDTH, Conf.PADDLE_HEIGHT)
    right_paddle = Paddle(Conf.WIDTH - 10 - Conf.PADDLE_WIDTH,
                          Conf.HEIGHT // 2 - Conf.PADDLE_HEIGHT // 2,
                          Conf.PADDLE_WIDTH, Conf.PADDLE_HEIGHT)
    ball = Ball(Conf.WIDTH // 2, Conf.HEIGHT // 2, Conf.BALL_RADIUS)
    power_up = PowerUp()
    paddles = [left_paddle, right_paddle]
    left_score = 0
    right_score = 0
    countdown(WIN)

    while run:
        clock.tick(Conf.FPS)
        draw(WIN, paddles, ball, left_score, right_score, power_up)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if left_score >= Conf.WINNING_SCORE:
            show_winner(WIN, "Left Player Won!")
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            power_up.reset_position()
            left_score = 0
            right_score = 0
            countdown(WIN)
            continue
        elif right_score >= Conf.WINNING_SCORE:
            show_winner(WIN, "Right Player Won!")
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            power_up.reset_position()
            left_score = 0
            right_score = 0
            countdown(WIN)
            continue

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)
        power_up.update(paddles, ball)

        if not power_up.active:
            power_up_rect = pygame.Rect(power_up.x - power_up.radius,
                                        power_up.y - power_up.radius,
                                        power_up.radius * 2,
                                        power_up.radius * 2)
            ball_rect = pygame.Rect(ball.x - ball.radius,
                                    ball.y - ball.radius,
                                    ball.radius * 2,
                                    ball.radius * 2)
            if power_up_rect.colliderect(ball_rect):
                power_up.apply_effect(paddles, ball)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            power_up.reset_position()
            if right_score < Conf.WINNING_SCORE:
                countdown(WIN)
        elif ball.x > Conf.WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            power_up.reset_position()
            if left_score < Conf.WINNING_SCORE:
                countdown(WIN)

    pygame.quit()

if __name__ == '__main__':
    main()
