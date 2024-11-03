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
import random

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
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
if len(joysticks) > 0:
    print(f"Found:")
else:
    print("No joysticks found")
for joystick in joysticks:
    print(f"  {joystick.get_name()}")
# Range is 0.0 to 1.0. Higher values require a larger movement of the stick to start moving the bat.
joystick_stickiness = 0.1

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
bat_speed_ppf = 10
bat_speed_ppm = bat_speed_ppf / mpf


# ball
ball = pygame.image.load("./images/football.png")
ball.convert_alpha()
ball_rect = ball.get_rect()
ball_start_center = screen.get_rect().center
ball_speed_ppf = (3.0, 3.0)
initial_ball_speed_ppm = (ball_speed_ppf[0] / mpf, ball_speed_ppf[1] / mpf)
current_ball_speed_ppm = initial_ball_speed_ppm
# When the ball is displayed at the start or after being missed, it
# remains static until ball_served is changed to True by hitting
# the space bar.
ball_served = False
ball_rect.center = ball_start_center

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
gapped_row_height = brick_rect.height + brick_gap_y
gapped_brick_width = brick_rect.width + brick_gap_x
block_set_width = (gapped_brick_width * brick_cols) - brick_gap_x
side_gap = (screen.get_width() - block_set_width) // 2
for row in range(brick_rows):
    brick_y = row * gapped_row_height
    for col in range(brick_cols):
        brick_x = side_gap + (col * gapped_brick_width)
        brick_locations.append((brick_x, brick_y))

#
# Run the game loop
#
clock = pygame.time.Clock()
game_over = False
while not game_over:
    dt = clock.tick(fps)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Handle events
    for event in pygame.event.get():
        if args.show_all_events:
            print(event)
        if event.type == pygame.QUIT:
            game_over = True

    # Process any keys (plural) that are pressed
    # This will update the bat and/or serve the ball

    joy_left = False
    joy_right = False
    joy_button_pressed = False
    for joystick in joysticks:
        joy_x = joystick.get_axis(0)
        if joy_x < -joystick_stickiness:
            joy_left = True
        elif joy_x > joystick_stickiness:
            joy_right = True
        num_buttons = joystick.get_numbuttons()
        for button_index in range(joystick.get_numbuttons()):
            button_value = joystick.get_button(button_index)
            if button_value > 0:
                joy_button_pressed = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or joy_left:
        desired_left_position = int(bat_rect.left - (bat_speed_ppm * dt))
        if desired_left_position > 0:
            bat_rect.left = desired_left_position
        else:
            bat_rect.left = 0
    if keys[pygame.K_RIGHT] or joy_right:
        desired_right_position = int(bat_rect.right + (bat_speed_ppm * dt))
        if desired_right_position < screen.get_width():
            bat_rect.right = desired_right_position
        else:
            bat_rect.right = screen.get_width()
    if (keys[pygame.K_SPACE] or joy_button_pressed) and not ball_served:
        ball_served = True
        current_ball_speed_ppm = initial_ball_speed_ppm
        # Randomize in which x direction the ball will be served.
        current_ball_speed_ppm = (current_ball_speed_ppm[0] * random.uniform(-1.0, 1.0), current_ball_speed_ppm[1])

    # Update the ball
    bat_hit_the_ball = False
    if ball_served:
        ball_rect.x += current_ball_speed_ppm[0] * dt
        ball_rect.y += current_ball_speed_ppm[1] * dt
        #
        # Check for collisions with the screen (or running off the bottom)
        # Notes that code only allows the ball to go all the way off the
        # screen on the bottom.
        #
        if ball_rect.left <= 0:
            # Left
            ball_rect.left = 0
            current_ball_speed_ppm = (current_ball_speed_ppm[0] * -1, current_ball_speed_ppm[1])
        elif ball_rect.top <= 0:
            # Top
            ball_rect.top = 0
            current_ball_speed_ppm = (current_ball_speed_ppm[0], current_ball_speed_ppm[1] * -1)
        elif ball_rect.right >= screen.get_width():
            # Right
            ball_rect.right = screen.get_width()
            current_ball_speed_ppm = (current_ball_speed_ppm[0] * -1, current_ball_speed_ppm[1])
        elif ball_rect.y > screen.get_height():
            # Bottom
            # If the ball goes off the bottom of the screen, reset it
            # The speed will be initialized when it is served during
            # event process of the space bar being hit.
            # Todo: The player should lose a life when this happens.
            ball_served = False
            ball_rect.center = ball_start_center
        #
        # Now check for collisions with the bat
        # If it hits clean on the top (meaning the whole ball is over the bat),
        # then just speed in the y direction is inverted. If, however it hits
        # while only some of the ball is over the bat, then the ball also
        # bounces in the x direction of the edge hit (right if it was the right
        # edge and left if it was the left edge). If top of the ball more than
        # half-way past the edge of the bat, then it only bounces in the x
        # direction and continues to fall.
        #
        #   Bat      Ball    Ball     Bat
        #   Left     Left    Right   Right
        #    |        |        |       |
        #    |        v        v       |
        #    |        +--------+       |
        #    v        | (Ball) |       v
        #    +--------+--------+-------+ <------ Bat Top
        #    |           Bat           | <------ Bat Center X
        #    +-------------------------+ <------ Bat Bottom
        #
        elif ball_rect.bottom >= bat_rect.top and ball_rect.top <= bat_rect.bottom:
            # This means a collision is possible
            if ball_rect.left >= bat_rect.left and ball_rect.right <= bat_rect.right:
                # Top
                current_ball_speed_ppm = (current_ball_speed_ppm[0], current_ball_speed_ppm[1] * -1)
                bat_hit_the_ball = True
            elif ball_rect.left < bat_rect.left <= ball_rect.right:
                # Left Side
                if ball_rect.top <= bat_rect.centery:
                    # Top Left
                    current_ball_speed_ppm = (abs(current_ball_speed_ppm[0]) * -1, current_ball_speed_ppm[1] * -1)
                    bat_hit_the_ball = True
                elif ball_rect.top <= bat_rect.bottom:
                    # Bottom Left
                    current_ball_speed_ppm = (abs(current_ball_speed_ppm[0]) * -1, current_ball_speed_ppm[1])
                    bat_hit_the_ball = True
            elif ball_rect.left <= bat_rect.right < ball_rect.right:
                # Right Side
                if ball_rect.top <= bat_rect.centery:
                    # Top Right
                    current_ball_speed_ppm = (abs(current_ball_speed_ppm[0]), current_ball_speed_ppm[1] * -1)
                    bat_hit_the_ball = True
                elif ball_rect.top <= bat_rect.bottom:
                    # Bottom Right
                    current_ball_speed_ppm = (abs(current_ball_speed_ppm[0]), current_ball_speed_ppm[1])
                    bat_hit_the_ball = True
            if bat_hit_the_ball:
                # The ball speeds up a little bit with each hit
                current_ball_speed_ppm = (current_ball_speed_ppm[0] * 1.01, current_ball_speed_ppm[1] * 1.01)
        #
        # Now check for collisions with any of the bricks
        #
        # When a brick is hit, delete it and bounce the ball in the direction
        # that it hit the brick.
        #
        #   Bat                       Bat
        #   Left                     Right
        #    |                         |
        #    v                         v
        #    +-------------------------+ <------ Brick Top
        #    |          Brick          |
        #    +--------+--------+-------+ <------ Brick Bottom
        #             | (Ball) |
        #             +--------+
        #             ^        ^
        #             |        |
        #            Ball    Ball
        #            Left    Right
        #
        deleted_bricks_locations = []
        for brick_location in brick_locations:
            # TODO: It may be better to store brick rect objects than a tuple of (x, y).
            brick_left, brick_top = brick_location
            brick_location_rect = pygame.Rect(brick_left, brick_top, brick_rect.width, brick_rect.height)
            if ball_rect.colliderect(brick_location_rect):
                deleted_bricks_locations.append(brick_location)
                #
                # Now bounce the ball in the direction(s) hit. Hits in the x and
                # y directions are check interdependently from each other to
                # handle corner hits.
                #
                if ball_rect.left <= brick_location_rect.left:
                    # Left
                    # Part of the ball is to the left of the brick. We already
                    # know it collided with the brick, so it must have hit along
                    # the left edge, or over the top left or under the bottom
                    # left corner.
                    current_ball_speed_ppm = (current_ball_speed_ppm[0] * -1, current_ball_speed_ppm[1])
                elif ball_rect.right >= brick_location_rect.right:
                    # Right
                    # Part of the ball is to the right of the brick. We already
                    # know it collided with the brick, so it must have hit along
                    # the right edge, or over the top right or under the bottom
                    # right corner.
                    current_ball_speed_ppm = (current_ball_speed_ppm[0] * -1, current_ball_speed_ppm[1])
                if ball_rect.top <= brick_location_rect.top:
                    # Top
                    # Part of the ball above the brick. We already
                    # know it collided with the brick, so it must have hit along
                    # the top edge, or over the top left or top right corner.
                    current_ball_speed_ppm = (current_ball_speed_ppm[0], current_ball_speed_ppm[1] * -1)
                elif ball_rect.bottom >= brick_location_rect.bottom:
                    # Bottom
                    # Part of the ball is below the brick. We already
                    # know it collided with the brick, so it must have it along
                    # the bottom edge, or under the top left or top right corner.
                    current_ball_speed_ppm = (current_ball_speed_ppm[0], current_ball_speed_ppm[1] * -1)

        for deleted_brick_location in deleted_bricks_locations:
            brick_locations.remove(deleted_brick_location)

    # Draw the bricks
    for brick_location in brick_locations:
        screen.blit(brick, brick_location)

    # Draw the bat
    screen.blit(bat, bat_rect)

    # Draw the ball
    screen.blit(ball, ball_rect)

    # Update the display to pick up what was drawn above for this frame
    pygame.display.update()

pygame.quit()
