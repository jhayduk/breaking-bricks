"""
The main file for the breaking-bricks game.

Note that all x and y values are in pixels.

Run with:

pipenv shell
python main.py

"""
import argparse
import pygame
#
# Parse any arguments passed in
#
parser = argparse.ArgumentParser(description="Run the Breaking Bricks game.")
parser.add_argument('--show-all-events', action='store_true', help='Show all Pygame events')
args = parser.parse_args()

#
# Init the pygame framework
#
pygame.init()

#
# Set up the game screen
#
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Breaking Bricks")

#
# Define desired frame rate in frames per second (fps)
# And calculate how many milliseconds per frame (mpf) that would correspond
# to if the frame rate were hit exactly. Note that mpf is a floating point value.
fps = 55
mpf = (1.0 / fps) * 1000

#
# Set up resources
#

# bat
bat = pygame.image.load("./images/paddle.png")
bat.convert_alpha()
bat_rect = bat.get_rect()
bat_rect.y = screen.get_height() - 100
# Bat speed is defined in pixels per frame (ppf) and then calculated into
# pixels per millisecond (ppm) so that it can be multiplied by the actual
# time between each from to move the bat.
bat_speed_pfm = 10
bat_speed_ppm = bat_speed_pfm / mpf


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
    dt_msecs = clock.tick(fps)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Handle events
    for event in pygame.event.get():
        if args.show_all_events:
            print(event)
        if event.type == pygame.QUIT:
            game_over = True

    # Process any keys (plural) that are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        desired_left_position = int(bat_rect.left - (bat_speed_ppm * dt_msecs))
        if desired_left_position > 0:
            bat_rect.left = desired_left_position
        else:
            bat_rect.left = 0
    if keys[pygame.K_RIGHT]:
        desired_right_position = int(bat_rect.right + (bat_speed_ppm * dt_msecs))
        if desired_right_position < screen.get_width():
            bat_rect.right = desired_right_position
        else:
            bat_rect.right = screen.get_width()

    # Draw the bricks
    for brick_location in brick_locations:
        screen.blit(brick, brick_location)

    # Draw the bat
    screen.blit(bat, bat_rect)

    # Update the display to pick up what was drawn above for this frame
    pygame.display.update()

pygame.quit()
