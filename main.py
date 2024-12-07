"""
The main file for the breaking-bricks game.

Notes:
    1. All x and y values are in pixels.
    2. Unless otherwise noted, all time is in milliseconds.

Run with:

pipenv shell
python main.py

"""
import argparse
import pygame

from Ball import Ball
from Brick import Brick
from ControllerInput import ControllerInput
from Paddle import Paddle
import score
from Tokens import Tokens

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
# Then calculate how many milliseconds per frame (mpf) would correspond to it
# if the frame rate were hit exactly each time.
#
fps = 55
mpf = (1 / fps) * 1000

#
# Check for joysticks and controllers
#
show_controller_status = False
controller_input = ControllerInput()

#
# Set up game elements
#
# These will be updated and drawn in the order they appear in the elements list
#
elements = []

# -------
# paddle
# -------
paddle = Paddle(x=0, y=screen.get_height() - 100)
elements.append(paddle)

# -------
# bricks
# -------

#
# The bricks are all assumed to be the same size, so the code creates one just
# to get the dimensions and then the brick is released.
#
sample_brick = Brick()
brick_gap = int(sample_brick.width * 0.10)
brick_rows = 5
brick_cols = screen.get_width() // (sample_brick.width + brick_gap)

#
# To even out the gap on the sides of the screen, the x gap on the last
# brick displayed needs to be ignored because it, effectively, is not part
# of the width of the set of blocks that are displayed. So, there is one
# less x gap than there are columns.
#
# To make things look somewhat symmetric and extra gap at the top of the
# set of bricks is added.
#
gapped_row_height = sample_brick.height + brick_gap
gapped_brick_width = sample_brick.width + brick_gap
block_set_width = (gapped_brick_width * brick_cols) - brick_gap
side_gap = (screen.get_width() - block_set_width) // 2
top_gap = side_gap

#
# With the calculations out of the way, release the sample_brick
# and create the set of bricks. These are saved in both the bricks
# list and the elements list.
#
del sample_brick
bricks = []
for row in range(brick_rows):
    brick_y = top_gap + (row * gapped_row_height)
    for col in range(brick_cols):
        brick_x = side_gap + (col * gapped_brick_width)
        new_brick = Brick(x=brick_x, y=brick_y)
        elements.append(new_brick)
        bricks.append(new_brick)

# -----
# ball
# -----
ball = Ball(x=screen.get_rect().centerx, y=screen.get_rect().centery, paddle=paddle)
elements.append(ball)

#
# Run the game loop
#
clock = pygame.time.Clock()
game_over = False
previous_brick_count = len(bricks)
while not game_over:
    dt = clock.tick(fps)

    # Clear the screen
    screen.fill((0, 0, 0))

    all_events = pygame.event.get()

    # Handle game level events
    for event in all_events:
        if args.show_all_events:
            print(event)
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            show_controller_status = not show_controller_status

    # Update the elements, including element level events
    for element in elements:
        element.update(dt=dt, events=all_events, screen=screen)

    # Check for and handle collisions between objects
    for element in [e for e in elements if e.collidable]:
        other_elements = [e for e in elements if e is not element and e.collidable]
        elements_collided_with_indexes = element.collidelistall(other_elements)
        for element_collided_with_index in elements_collided_with_indexes:
            element.collided_with(other_elements[element_collided_with_index])

    #
    # Remove any bricks that were hit
    #
    # Note that clearing the bricks_to_delete at the end is not technically
    # needed because it will get cleared on the next iteration. However, it
    # feels cleaner to explicitly free the last references to the now deleted
    # bricks rather than let it happen in the future as a side effect.
    #
    bricks_to_delete = []
    for brick in bricks:
        if brick.was_hit:
            bricks_to_delete.append(brick)
    for brick in bricks_to_delete:
        bricks.remove(brick)
        elements.remove(brick)
    bricks_to_delete = []

    #
    # Check if there are _now_ no more bricks, which means that the screen was
    # cleared in this frame.
    #
    if len(bricks) == 0 and previous_brick_count != 0:
        score.screen_cleared(ball.velocity)
    previous_brick_count = len(bricks)

    # Draw the scoreboard items
    Tokens.draw(screen)
    score.draw(screen)

    # Draw the elements
    for element in elements:
        element.draw(screen)

    # Draw any debug elements
    if show_controller_status:
        controller_input.show_current_state(screen)

    # Update the display to pick up what was drawn above for this frame
    pygame.display.update()

pygame.quit()
