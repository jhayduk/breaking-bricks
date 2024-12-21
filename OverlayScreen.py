import pygame
from pygame import Surface
from pygame.color import Color
from pygame.math import Vector2
from typing import override

from GameElement import GameElement


class GameOver(GameElement):
    """
    GameOver is a GameElement that is instantiated when the player runs out of
    tokens. It is intended to exist as the last element in the list of game
    elements so that it gets drawn last. It will place a translucent overlay
    on the game screen so that what is drawn there is "greyed out", and then
    will display the words "Game Over" on to of it.
    """
    def __init__(self, screen: Surface):
        """
        When instantiated, the __init__ method is passed the screen surface
        object so that it can overlay itself on top of it.

        :param Surface screen: The game screen that should be greyed out and
                                where the "Game Over" message will appear.
                                During initialization, this is used to get the
                                size of the screen.
        """
        # Create the semi-transparent overlay
        overlay = Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # RGBA: Black with 50% transparency

        # Add the Game Over text
        font = pygame.font.SysFont("Arial", 72, bold=True)
        text = font.render("Game Over", True, Color("white"))
        text_rect = text.get_rect()
        text_rect.center = screen.get_rect().center
        overlay.blit(text, text_rect)

        #
        # Initialize the base GameElement class items. The overlay becomes the
        # image that is displayed at every frame.
        #
        super().__init__(overlay, x=0, y=0, velocity=Vector2(0, 0), collidable=False)


    @override
    def update(self, *args, **kargs):
        """
        The GameOver object stays once displayed, so the GameElement update
        method is bypassed.
        """
        pass

    @override
    def collided_with(self, other_element: GameElement):
        """
        The GameOver object does not participate in collision detectioon,
        so this is bypassed.
        """
        pass

    #
    # GameElement's draw() method is sufficient for the GameOver screen, so it
    # is used as is.
    #
