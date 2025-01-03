"""
Brick

A Brick is a GameElement that is displayed towards the top of the game
screen. When hit by the ball, it disappears.

A Brick is a subclass of GameElement, which means it is updatable and
drawable on the game screen.

A Brick has x and y positions (as well as the topleft, bottom, etc. variables
because it is ultimately a subclass of Rect).

The x and y positions are always defined in pixels and refer to the top left
corner of the image. The x and y values are always relative to the top left
corner of the game screen itself, which is defined to be at x=0, y=0. Once
placed, bricks do not move.

As a subclass of GameElement, a Brick also has a velocity. However, bricks do
not move, so the velocity is always (0, 0) and does not change.
"""
import pygame
from pygame import Vector2
from typing import override

from arcade_tools.GameElement import GameElement
import score

_BRICK_IMAGE_FILE="./images/brick.png"


class Brick(GameElement):

    was_hit = False
    """
    This becomes set to True if this brick has been hit by the ball.
    This value should not be written by any other code, but should be read to
    see if references to this object should be dropped so that the brick
    is no longer displayed and the memory used by this object can be freed.
    """

    def __init__(self, x: int = 0, y: int = 0):
        """
        Other than making sure pygame has been initialized and supplying
        the image file name, the parent GameElement __init__ method does
        everything that is required to create a Brick.
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
        # Initialize the base GameElement class items.
        #
        # The velocity of a GameElement defaults to (0, 0), but set it here
        # to be explicit and to guarantee that it is not moving when created.
        #
        super().__init__(_BRICK_IMAGE_FILE, x=x, y=y, velocity=Vector2(0, 0))

        #
        # Right now, all bricks have the same base value
        #
        self._base_value = 1

    @override
    def update(self, *args, **kargs):
        """
        Because a Brick never moves, there is nothing to update. Intentionally
        override the update method with an empty method to avoid wasting time
        with the calculations made by GameElement.update().
        """
        pass

    @override
    def collided_with(self, other_element: GameElement):
        """
        Because of how the game is constructed, the only object that can
        collide with a brick is the ball. In the game, when that happens,
        the brick should disappear. In this code, Set the was_hit attribute so
        that the main game loop can drop the reference to this object so it
        can be deleted and no longer displayed.
        """
        self.was_hit = True

        score.brick_destroyed( self._base_value, other_element.velocity)

    #
    # GameElement's draw() method is sufficient for Brick objects, so that is NOT overridden
    #
