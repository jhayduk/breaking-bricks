"""
The main file for the breaking-bricks game.

Run with:

pipenv shell
python main.py

"""
import pygame

pygame.init()

#
# Set up the game screen
#
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Breaking Bricks")

#
# Set up resources
#
bat = pygame.image.load("./images/paddle.png")
bat.convert_alpha()
bat_rect = bat.get_rect()

ball = pygame.image.load("./images/football.png")
ball.convert_alpha()
ball_rect = ball.get_rect()

brick = pygame.image.load("./images/brick.png")
brick.convert_alpha()
brick_rect = brick.get_rect()

#
# Run the game loop
#
clock = pygame.time.Clock()
game_over = False
while not game_over:
    dt = clock.tick(55)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

pygame.quit()
