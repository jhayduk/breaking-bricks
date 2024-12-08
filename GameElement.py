import pygame
from pygame import Surface
from pygame.event import Event
from pygame.math import Vector2
from typing import Union


class GameElement(pygame.Rect):
    """
    A GameElement is an updatable and drawable entity. It is a subclass of Rect,
    so it has x and y positions (as well as the topleft, bottom, etc. variables
    that Rect objects have). It also has an image (instantiated with a filename),
    and a velocity in 2D space.

    Public Methods (in addition to those inherited from Rect):

        update(dt, events, screen)
        collided_with(other_element)
        draw(screen)

    Public Instance Variables (in addition to those inherited from Rect):

        velocity - The current velocity of this element on the screen in pixels
                    per millisecond. The positive direction of a velocity
                    vector is to the right and down (↘).

        collidable - True if this element can be collided with and, therefore,
                        should participate in collision detection calculations.

    The x and y positions are always defined in pixels and refer to the top left
    corner of the image. The x and y values are always relative to the top left
    corner of the game screen itself, which is defined to be at x=0, y=0.

    The velocity is a Vector2 value in pixels per millisecond (ppm), with a unit
    vector pointing 1 ppm to the right and 1 ppm down (↘).

    The image file is expected to contain a single loadable image that can be
    drawn on the pygame screen. A single image can be selected from a sprite sheet
    of multiple images by using optional cropping parameters when instantiating
    the object

    While not required, it is expected that the update, collided_with, and draw
    methods are called once per frame, in the following order:

      1. update
      2. collided_with
      3. draw

    All of these methods are normally overridden in subclasses of this class,
    but this class' version can be used for simple elements.
    """
    def __init__(self,
                 image: Union[str, Surface],
                 x: int = 0,
                 y: int = 0,
                 velocity: Vector2 = Vector2(0, 0),
                 collidable: bool = True):
        """
        :param image: The name of the file, including the relative path
                        to the file that contains the image to be displayed
                        for the element, or a pygame.Surface object. If the
                        name of a file is given, it is assumed to contain
                        alpha information for transparency. The surface
                        created from this image will have the convert_alpha
                        method called on it to improve blit performance.
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
        :param collidable: If True (the default) the element can be collided
                            with and should participate in collision detection
                            calculations. Set this to False for background
                            elements or anything that other elements can
                            pass through without hitting anything.

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

        # Load the image if a file path is provided, otherwise use the provided surface
        if isinstance(image, str):
            self.image = pygame.image.load(image).convert_alpha()
        elif isinstance(image, Surface):
            self.image = image
        else:
            raise ValueError("The image parameter must be either a file path or a pygame.Surface object.")

        image_rect = self.image.get_rect()

        # Initialize the Rect with the size of the image
        super().__init__(x, y, image_rect.width, image_rect.height)

        # Initialize other passed in settings
        self.velocity = velocity
        self.collidable = collidable

    def update(self, dt: int, events: list[Event] = None, screen: Surface = None):
        """
        Update the position of the GameElement based on its velocity and the time delta.

        Warning: If overridden, this method should be overridden completely.
                    (i.e. do NOT use super().update())

        :param dt: The number of milliseconds since the last call to update.
                    This is used with any movement calculations to help
                    smooth and jitter in the frame rate.
        :param events: A list of the pygame events detected since the last
                        frame. Not all elements care about events, so this
                        is optional and defaults None if omitted. When
                        overriding this method, the fact that the events can
                        be None MUST be taken into account if it is used.
        :param screen: The surface on which this GameElement will ultimately be
                        drawn. This can be used to determine if this element
                        will still be on the screen when drawn. Not all
                        elements care about the surface, so it is optional
                        and defaults to None if omitted. When overriding
                        this method, the fact that the screen can be None
                        MUST be taken into account if it is used.

        """
        self.move_ip(self.velocity.x * dt, self.velocity.y * dt)

    def collided_with(self, other_element: 'GameElement'):
        """
        When two objects collide with each other, they both can be affected.

        This method should be called whenever collisions occur.

        The "other_element" is what collided with the self instance.

        Override this method if the self object should be affected by
        collisions and use it to update the self instance only. Do not update
        the "other_instance". If the "other_instance" is also affected by the
        collision, its collided_with() method is the one that is responsible
        for updating that object.

        :param other_element: The GameElement object that collided with this
                                GameElement.
        """
        # TODO: Provide some generic reaction to collisions
        pass

    def draw(self, screen: Surface):
        """
        Draw this object's image on the given screen surface at its current position.

        Warning: If overridden, this method should be overridden completely.
                    (i.e. do NOT use super().update())

        :param screen: The display surface this GameElement is to be drawn in.
            The element's position is always relative to the top-left corner
            of the screen.
        """
        screen.blit(self.image, self.topleft)
