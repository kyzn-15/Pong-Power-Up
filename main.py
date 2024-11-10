import pygame
import random
from conf import Conf  
from sprites.paddle import Paddle
from sprites.ball import Ball

pygame.init()

WIN = pygame.display.set_mode((Conf.WIDTH, Conf.HEIGHT))
pygame.display.set_caption("Pong")

def draw(win, paddles, ball, left_score, right_score, power_up):
    win.fill(Conf.BLACK)
    left_score_text = Conf.SCORE_FONT.render(f"{left_score}", 1, Conf.WHITE)
    right_score_text = Conf.SCORE_FONT.render(f"{right_score}", 1, Conf.WHITE)
    win.blit(left_score_text, (Conf.WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (Conf.WIDTH * (3 / 4) - right_score_text.get_width() // 2, 20))
    for paddle in paddles:
        paddle.draw(win)
    for i in range(10, Conf.HEIGHT, Conf.HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, Conf.WHITE, (Conf.WIDTH // 2 - 5, i, 10, Conf.HEIGHT // 20))
    ball.draw(win)
    
    
    if power_up:
        pygame.draw.rect(win, Conf.WHITE, (power_up["x"], power_up["y"], Conf.POWER_UP_SIZE, Conf.POWER_UP_SIZE))
    
    pygame.display.update()

def spawn_power_up():
    x = random.randint(Conf.WIDTH // 4, Conf.WIDTH * 3 // 4)
    y = random.randint(Conf.HEIGHT // 4, Conf.HEIGHT * 3 // 4)
    power_type = random.choice(Conf.POWER_UP_TYPES)
    return {"x": x, "y": y, "type": power_type}

def apply_power_up(power_up, left_paddle, right_paddle, ball):
    if power_up["type"] == "increase_paddle_size":
        left_paddle.height *= 1.5
        right_paddle.height *= 1.5
    elif power_up["type"] == "increase_ball_speed":
        ball.x_vel *= 1.5
        ball.y_vel *= 1.5

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= Conf.HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= Conf.HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= Conf.HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, Conf.HEIGHT // 2 - Conf.PADDLE_HEIGHT // 2, Conf.PADDLE_WIDTH, Conf.PADDLE_HEIGHT)
    right_paddle = Paddle(Conf.WIDTH - 10 - Conf.PADDLE_WIDTH, Conf.HEIGHT // 2 - Conf.PADDLE_HEIGHT // 2, Conf.PADDLE_WIDTH, Conf.PADDLE_HEIGHT)
    ball = Ball(Conf.WIDTH // 2, Conf.HEIGHT // 2, Conf.BALL_RADIUS)
    left_score = 0
    right_score = 0
    power_up = spawn_power_up()

    while run:
        clock.tick(Conf.FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score, power_up)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        
        if power_up and power_up["x"] < ball.x < power_up["x"] + Conf.POWER_UP_SIZE and power_up["y"] < ball.y < power_up["y"] + Conf.POWER_UP_SIZE:
            apply_power_up(power_up, left_paddle, right_paddle, ball)
            power_up = spawn_power_up()  

        
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > Conf.WIDTH:
            left_score += 1
            ball.reset()

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
            power_up = spawn_power_up()  

    pygame.quit()

if __name__ == '__main__':
    main()
