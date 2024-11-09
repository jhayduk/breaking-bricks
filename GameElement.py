"""
GameElement

A GameElement is an updatable and drawable entity. It is a subclass of Rect,
so it has x and y positions (as well as the topleft, bottom, etc. variables
that Rect objects have). It also has an image (instantiated with a filename),
and a velocity in 2D space.

The x and y position are always defined in pixels and refer to the top left
corner of the image on the screen. This value is always relative to the top
left corner of the screen which is defined to be at x=0, y=0.

The velocity is a Vector2 value in pixels per millisecond (ppm), with a unit
vector pointing 1 ppm to the right and 1 ppm down (↘).

The image file is expected to contain a single loadable image that can be
drawn on the pygame screen. A single image can be selected from a sprite sheet
of multiple images by using optional cropping parameters when instantiating
the object

While not required, it is expected that the update and draw method are called
once per frame, and that update is called before draw each time.

Both update and draw are normally overridden in subclasses of GameElement,
but this class' version can be used for simple elements.
"""
from typing import overload

import pygame
from pygame.math import Vector2
from typing import override


class GameElement(pygame.Rect):
    #
    # The current velocity of this element on the screen in pixels per millisecond
    # The positive direction of a velocity vector is to the right and down (↘)
    #
    velocity: Vector2

    def __init__(self,
                 image_file: str,
                 x: int = 0,
                 y: int = 0,
                 velocity: Vector2 = Vector2(0, 0)):
        """
        :param image_file: The name of the file, including the relative path
                    to the file that contains the image to be displayed for
                    the element. While not necessary, it is assumed to
                    contain alpha information for transparency. The surface
                    created from this image will have the convert_alpha
                    method called on it to improve blit performance.
        :param x: The initial horizontal position, in pixels, relative to the
                    top left of the screen, of the element.
        :param y: The initial vertical position, in pixels, relative to the
                    top left of the screen, of the element.
        :param velocity: The initial velocity, in pixels per millisecond,
                    of the element. The unit vector points to the right and
                    down.

        TODO: Add support for cropping a single image out of a sprite sheet.
        """
        #
        # Make sure pygame is initialized. Normally, this is expected to be
        # done before elements are created, so issue a warning if it had to
        # be done here.
        #
        if not pygame.get_init():
            print(f"WARNING: pygame was not initialized when a {self.__class__.__name__} object was instantiated. It has now been initialized, but pygame.init() should normally be called before instantiating any instances of the {self.__class__.__name__} class.")
            pygame.init()

        # Load the image
        self.image = pygame.image.load(image_file).convert_alpha()
        image_rect = self.image.get_rect()

        # Initialize the Rect with the size of the image
        super().__init__(x, y, image_rect.width, image_rect.height)

        # Initialize the velocity
        self.velocity = velocity

    def update(self, dt: int):
        """
        Update the position of the GameElement based on its velocity and the time delta.

        :param dt: The time delta in milliseconds since the last update.
        """
        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

    def draw(self, screen: pygame.Surface):
        """
        Draw this object's image on the given screen surface at its current position.

        :param screen: The display surface this GameElement is to be drawn in.
            The element's position is always relative to the top-left corner
            of the screen.
        """
        screen.blit(self.image, self.topleft)