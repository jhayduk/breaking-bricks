"""
The main file for the breaking-bricks game.

Note that all x and y values are in pixels.

Run with:

pipenv shell
python main.py

"""
import pygame

pygame.init()

#
# Set up the game screen
#
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breaking Bricks")

#
# Set up resources
#

# bat
bat = pygame.image.load("./images/paddle.png")
bat.convert_alpha()
bat_rect = bat.get_rect()

# ball
ball = pygame.image.load("./images/football.png")
ball.convert_alpha()
ball_rect = ball.get_rect()

# bricks
brick = pygame.image.load("./images/brick.png")
brick.convert_alpha()
brick_rect = brick.get_rect()
brick_locations = []
brick_gap_x = 10
brick_gap_y = 10
brick_rows = 5
brick_cols = screen.get_width() // (brick.get_width() + brick_gap_x)
# To even out the gap on the sides of the screen, the x gap on the last
# brick displayed needs to be ignored because it, effectively, is not part
# of the width of the set of blocks that are displayed. So, there is one
# less x gap than there are columns.
block_set_width = ((brick.get_width() + brick_gap_x) * brick_cols) - brick_gap_x
side_gap = (screen.get_width() - block_set_width) // 2

for row in range(brick_rows):
    brick_y = row * (brick_rect.height + brick_gap_y)
    for col in range(brick_cols):
        brick_x = side_gap + (col * (brick_rect.width + brick_gap_x))
        brick_locations.append((brick_x, brick_y))

#
# Run the game loop
#
clock = pygame.time.Clock()
game_over = False
while not game_over:
    dt = clock.tick(55)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the bricks
    for brick_location in brick_locations:
        screen.blit(brick, brick_location)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Update the display to pick up what was drawn above for this frame
    pygame.display.update()

pygame.quit()
