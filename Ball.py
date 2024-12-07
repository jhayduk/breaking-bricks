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
from Tokens import Tokens
from typing import override

from ControllerInput import ControllerInput
from GameElement import GameElement
from Paddle import Paddle

_BALL_IMAGE_FILE="./images/football.png"
_INITIAL_BALL_SPEED_PPM = 0.25
_MINIMUM_BALL_Y_VELOCITY_PPM = _INITIAL_BALL_SPEED_PPM
_MAX_SERVE_ANGLE_DEGREES = 60
_PADDLE_TO_BALL_HORIZONTAL_VELOCITY_TRANSFER_RATIO = 0.10
_SPEED_INCREASE_RATIO_AFTER_OBJECT_HIT = 1.01


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

        #
        # Save off the paddle pointer for use in collision detection
        #
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
        Update the position of the ball and check for collisions or if it has
        gone off the bottom of the screen. If the ball has not yet started
        moving, check to see if it is being served in this frame.

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
                # that it is not moving straight down because it can be a
                # little tricky to get it to deflect to the side off of the
                # paddle, especially if the user does not realize there is a
                # way to do it.
                #
                serve_angle_degrees = random.randrange(-_MAX_SERVE_ANGLE_DEGREES, _MAX_SERVE_ANGLE_DEGREES)
                if abs(serve_angle_degrees) < 15:
                    serve_angle_degrees = math.copysign(15, serve_angle_degrees)
                self.velocity.rotate_ip(serve_angle_degrees)
            else:
                return

        # Update the ball's position
        self.move_ip(self.velocity.x * dt, self.velocity.y * dt)

        screen_rect = screen.get_rect()

        #
        # Check if the ball ran off the bottom of the screen
        # Wait for the top of the ball to disappear under the screen so
        # that it can be seen falling off the screen.
        # The player loses a token every time this happens.
        #
        if self.top > screen_rect.bottom:
            self.topleft = (self._starting_x, self._starting_y)
            self.velocity = Vector2(0, 0)
            self._has_been_served = False
            Tokens.lose(1)

        # Handle collisions with the sides and top of the screen
        if self.left < screen_rect.left:
            self.velocity.x = abs(self.velocity.x)
        elif self.right > screen_rect.right:
            self.velocity.x = -abs(self.velocity.x)
        if self.top < screen_rect.top:
            self.velocity.y = abs(self.velocity.y)

    @override
    def collided_with(self, other_element: GameElement):
        """
        The ball can collide with the paddle, or one (or more) of the bricks.
        The reaction is always the same. The ball will bounce away from the
        edge(s) that it just hit. Additionally, the ball will gain a portion
        of the horizontal velocity of the paddle if it collides with it.
        As a simplification, since bricks are stationary, the code will
        add a portion of the horizontal velocity of anything that the ball
        hits.

        Also, everytime the ball hits an object, any object, it speeds up
        slightly. This makes the game more challenging as time goes on.
        """
        # Completely enclosed
        if other_element.contains(self):
            self.velocity.y = abs(self.velocity.y)
        else:
            # bottom
            if self.bottom > other_element.bottom:
                self.velocity.y = abs(self.velocity.y)
            # top
            elif self.top < other_element.top:
                self.velocity.y = -abs(self.velocity.y)
            # right
            if self.right > other_element.right:
                self.velocity.x = abs(self.velocity.x)
            # left
            elif self.left < other_element.left:
                self.velocity.x = -abs(self.velocity.x)

        # Transfer a small amount of the x velocity of the other_object to the ball.
        self.velocity.x += _PADDLE_TO_BALL_HORIZONTAL_VELOCITY_TRANSFER_RATIO * other_element.velocity.x

        # Speed up the ball slightly
        self.velocity.scale_to_length(self.velocity.length() * _SPEED_INCREASE_RATIO_AFTER_OBJECT_HIT)

        #
        # Lastly, if the y velocity should ever be nearly 0,
        # it could be impossible for the ball to move. If, somehow,
        # is condition were to occur, raise the velocity to the
        # minimum amount in the direction of motion or down, if there
        # is exactly 0 velocity in the y direction.
        #
        if -_MINIMUM_BALL_Y_VELOCITY_PPM < self.velocity.y < _MINIMUM_BALL_Y_VELOCITY_PPM:
            self.velocity.y = -_MINIMUM_BALL_Y_VELOCITY_PPM if self.velocity.y < 0 else _MINIMUM_BALL_Y_VELOCITY_PPM
        # TODO - Except for the speed up, these reflection calculations are generic for an elastic self colliding with an immovable other_element

    #
    # GameElement's draw() method is sufficient for Ball objects, so that is NOT overridden
    #
