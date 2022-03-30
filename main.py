# Physics Gravitation simulation

import pygame
from constants import *
from physics import *

pygame.init()

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Collision Simulation")


balls = []

for i in range(NO_OF_BALLS):
    new_ball = Ball(balls) # Random Initial postion and Random Initial velocity is given to the ball
    balls.append(new_ball)

def draw_display(balls):
    gameDisplay.fill(BLACK)
    for ball in balls:
        pygame.draw.circle(gameDisplay, ball.color, (ball.x, ball.y), BALL_RADIUS)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        Ball.motion(balls)
        Ball.ballCollision(balls)
        draw_display(balls)
    pygame.quit()


if __name__=='__main__':
    main()