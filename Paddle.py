"""
Paddle

The Paddle is a GameElement moves back and forth near the bottom of screen and
is used to deflect the ball to both keep it in play and in an attempt to break
the bricks by bouncing the ball into them.

The Paddle is a subclass of GameElement, which means it is updatable and
drawable on the game screen.

It has x and y positions (as well as the topleft, bottom, etc. variables
because it is ultimately a subclass of Rect).

The x and y positions are always defined in pixels and refer to the top left
corner of the image. The x and y values are always relative to the top left
corner of the game screen itself, which is defined to be at x=0, y=0.

The velocity is a Vector2 value in pixels per millisecond (ppm), with a unit
vector pointing 1 ppm to the right and 1 ppm down (↘).

For the paddle, the velocity is always only in the x direction. For moving
the paddle itself, a velocity is not really needed. However, it is calculated
and updated so that it can be transferred to the ball when the ball is hit.
"""
import pygame
from pygame import Surface
from typing import override

from GameElement import GameElement
from ControllerInput import ControllerInput

_PADDLE_IMAGE_FILE="./images/paddle.png"
_MAX_PADDLE_SPEED_PPM = 0.55


class Paddle(GameElement):
    # The single instance of the paddle. This is intended to be used internally only.
    _instance = None

    #
    # A flag to make sure that later calls do not reset anything.
    # This is intended to be used internally only.
    #
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        """
        Make the Paddle a singleton class since there will only ever be one
        of them. This also allows the ball class access the paddle when
        checking if it collided with it.

        TODO: Is there a way to not have multiple users of the paddle object?
        """
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, x, y):
        if not self._is_initialized:
            #
            # Make sure pygame is initialized. Normally, this is expected to be
            # done before elements are created, so issue a warning if it had to
            # be done here.
            #
            if not pygame.get_init():
                print(f"WARNING: pygame was not initialized when a {self.__class__.__name__} object was instantiated. It has now been initialized, but pygame.init() should normally be called before instantiating any instances of the {self.__class__.__name__} class.")
                pygame.init()

            #
            # Grab a local pointer to the singleton ControllerInput object so that
            # it does not need to be re-created everytime the update() method is
            # called.
            #
            self._controller_input = ControllerInput()

            #
            # Now, initialize the base GameElement class items.
            #
            super().__init__(_PADDLE_IMAGE_FILE, x=x, y=y)

            #
            # And set the self._is_initialized flag so later calls to get this
            # singleton do not end up re-initializing the structures.
            #
            self._is_initialized = True

    @override
    def update(self, dt: int, screen: Surface = None, **kwargs):
        """
        :param dt: The number of milliseconds since the last call to update.
                    This is used with any movement calculations to help
                    smooth and jitter in the frame rate.
        :param screen: The screen the paddle will be drawn on. This is used to
                        make sure the paddle does not go off the screen and
                        MUST be supplied.
        :param kwargs: Any other key word arguments, such as events, are
                        ignored by this method.
        """
        # Check that required parameters have been supplied
        assert screen is not None , f"INTERNAL ERROR: A screen parameter MUST be supplied to the {self.__class__.__name__}.update() method"

        self.velocity.x = self._controller_input.paddle() * _MAX_PADDLE_SPEED_PPM
        self.x += self.velocity.x * dt

        #
        # Check to make sure the updated position does not place any part of
        # the paddle off the screen. If it does, put the paddle right at the
        # edge that it would have gone past.
        #
        screen_rect = screen.get_rect()
        self.left = max(self.left, screen_rect.left)
        self.right = min(self.right, screen_rect.right)

    @override
    def collided_with(self, other_element: GameElement):
        """
        The paddle itself does not react to being collided with, so anything
        that the generic GameElement method might do is bypassed.
        """
        pass

    #
    # The draw method of the base GameElement class is used without modification for the Paddle
    #
