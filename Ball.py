"""
Ball

The Ball is a GameElement starts the game at the starting position. When a
a start button is pressed it then starts falling in a semi-random direction
and then can bounce off of the paddle, the top and side of the screen and the
bricks. If the ball hits a brick, it bounces off of it, but the brick "breaks"
and disappears. If the ball falls off the bottom of the screen, it resets to
the starting position.

A Ball is a subclass of GameElement, which means it is updatable and
drawable on the game screen.

A Ball has x and y positions (as well as the topleft, bottom, etc. variables
because it is ultimately a subclass of Rect) and a velocity.

The x and y positions are always defined in pixels and refer to the top left
corner of the image. The x and y values are always relative to the top left
corner of the game screen itself, which is defined to be at x=0, y=0.

The velocity is a Vector2 value in pixels per millisecond (ppm), with a unit
vector pointing 1 ppm to the right and 1 ppm down (↘).

Although the game starts with a single ball, this class is NOT designed as a
singleton, allowing for the possibility of multiple balls in future updates.
"""
import math
import pygame
from pygame import Surface
from pygame import Vector2
import random
from typing import override

from ControllerInput import ControllerInput
from GameElement import GameElement
from Paddle import Paddle

_BALL_IMAGE_FILE="./images/football.png"
_INITIAL_BALL_SPEED_PPM = 0.25
_MAX_SERVE_ANGLE_DEGREES = 60
_PADDLE_TO_BALL_HORIZONTAL_VELOCITY_TRANSFER_RATIO = 0.10
_SPEED_INCREASE_RATIO_AFTER_PADDLE_HIT = 1.01


class Ball(GameElement):

    def __init__(self, x: int, y: int, paddle: Paddle):
        """
        In addition to the standard starting x and y coordinates, the
        constructor also requires a Paddle object to be passed to it, which it
        will retain. This object is used to see if the ball collided with the
        paddle and is passed in here to make it explicit in the main routine
        that there is a dependency.

        :param x:
        :param y:
        :param paddle:
        """
        #
        # Make sure pygame is initialized. Normally, this is expected to be
        # done before elements are created, so issue a warning if it had to
        # be done here.
        #
        if not pygame.get_init():
            print(
                f"WARNING: pygame was not initialized when a {self.__class__.__name__} object was instantiated. It has now been initialized, but pygame.init() should normally be called before instantiating any instances of the {self.__class__.__name__} class.")
            pygame.init()

        #
        # Grab a local pointer to the singleton ControllerInput object so that
        # it does not need to be re-created everytime the update() method is
        # called. This is used to see if the serve button has been pressed.
        #
        self._controller_input = ControllerInput()

        # Save off the paddle pointer for use in collision detection
        self._paddle = paddle

        #
        # Record that this ball has not yet been served and should not
        # be moving. Since velocity has floating point components, the code
        # cannot rely on it being (0, 0) to know that it is stopped.
        #
        self._has_been_served = False

        #
        # Record the starting position
        #
        self._starting_x = x
        self._starting_y = y

        #
        # Finally, initialize the base GameElement class items.
        #
        # The velocity of a GameElement defaults to (0, 0), but set it here
        # to be explicit and to guarantee that it is not moving when created.
        #
        super().__init__(_BALL_IMAGE_FILE, x=x, y=y, velocity=Vector2(0, 0))

    @override
    def update(self, dt: int, screen: Surface = None, **kwargs):
        """
        :param dt: The number of milliseconds since the last call to update.
                    This is used with any movement calculations to help
                    smooth and jitter in the frame rate.
        :param screen: The screen the ball will be drawn on. This is used
                        to see if the ball should bounce off the top or
                        sides, or if it should go of the bottom of the
                        screen.
        :param kwargs: Any other key word arguments, such as events, are
                        ignored by this method.
        """
        # Check that required parameters have been supplied
        assert screen is not None , f"INTERNAL ERROR: A screen parameter MUST be supplied to the {self.__class__.__name__}.update() method"

        if not self._has_been_served:
            """
            Check if the serve button has been hit. If so, then change the
            state to serve the ball and continue on with the rest of the
            update code. If not, then just return since there is nothing
            to update.
            """
            if self._controller_input.serve():
                self._has_been_served = True
                self.velocity = Vector2(0.0, _INITIAL_BALL_SPEED_PPM)
                #
                # Randomly deflect the ball in the x direction and make sure
                # that it is not moving straight down because, with the way
                # it bounces off the paddle, it will be very difficult, if
                # not impossible, to get it moving in the x direction at all.
                #
                serve_angle_degrees = random.randrange(-_MAX_SERVE_ANGLE_DEGREES, _MAX_SERVE_ANGLE_DEGREES)
                if abs(serve_angle_degrees) < 5:
                    serve_angle_degrees = math.copysign(5, serve_angle_degrees)
                self.velocity.rotate_ip(serve_angle_degrees)
            else:
                return

        # Update the ball's position
        self.move_ip(self.velocity.x * dt, self.velocity.y * dt)

        screen_rect = screen.get_rect()

        #
        # Check if the ball ran off the bottom of the screen
        # Wait for the top of the ball to disappear under the screen so
        # that it can be seen falling off the screen
        #
        if self.top > screen_rect.bottom:
            self.topleft = (self._starting_x, self._starting_y)
            self.velocity = Vector2(0, 0)
            self._has_been_served = False

        #
        # Handle collisions with the top of the paddle
        #
        # When the ball hits the top paddle, it reflects up. To keep the ball
        # from getting stuck on the paddle, don't simply invert y, actually
        # set it to be negative.
        #
        # If the paddle is moving at the time of the hit, add some of the
        # horizontal velocity of the paddle to the ball. This provides some
        # way to affect the angle the ball is moving in. Note that not all the
        # horizontal velocity of the paddle is added because it can speed the
        # ball up way too quickly.
        #
        # That said, when the ball hits the paddle, the ball should always
        # speed up slightly to make the game harder as time goes on.
        #
        #  Paddle    Ball    Ball    Paddle
        #   Left     Left    Right   Right
        #    |        |        |       |
        #    |        v        v       |
        #    |        +--------+       |
        #    v        | (Ball) |       v
        #    +--------+--------+-------+
        #    |          Paddle         |
        #    +-------------------------+
        #
        if self.colliderect(self._paddle) and self.top <= self._paddle.top:
            self.velocity.y = -abs(self.velocity.y)
            self.velocity.x += _PADDLE_TO_BALL_HORIZONTAL_VELOCITY_TRANSFER_RATIO * self._paddle.velocity.x
            self.velocity.scale_to_length(self.velocity.length() * _SPEED_INCREASE_RATIO_AFTER_PADDLE_HIT)

        # Handle collisions with the sides and top of the screen
        if self.left < screen_rect.left:
            self.velocity.x = abs(self.velocity.x)
        elif self.right > screen_rect.right:
            self.velocity.x = -abs(self.velocity.x)
        if self.top < screen_rect.top:
            self.velocity.y = abs(self.velocity.y)
