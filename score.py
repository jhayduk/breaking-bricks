"""
The score is displayed on the bottom right of the screen and is rendered after
any background is drawn and before any of the game elements are drawn. This
way, if the ball happens to travel past it, the ball will be displayed on top
of the score as if it is passing over it.

The score is an integer that goes up for every brick that is hit. The amount
that it goes up is a function of the speed of the ball at the time. This way,
as the game gets harder, the score goes up more for each hit. It also goes up
by a larger amount when all the bricks have removed.

At some point in the future, if there are multiple levels, the number of
points for each hit, and for clearing the screen, can be a factor of the
level as well.
"""
import math
import pygame
from pygame import Surface
from pygame.color import Color
from pygame.math import Vector2

_FONT_NAME = "Arial"
_FONT_SIZE = 24
_TEXT_COLOR = Color('white')

_SPEED_FACTOR = math.sqrt(1000)
"""
The value of the speed of the ball can be quite small because the velocity
is in pixels per millisecond. The score calculation will use the squared
magnitude of the velocity for efficiency, so the value used for the
_SPEED_FACTOR is the sqrt(1000) to make the speed value used for the score,
more or less, in the pixels per second range.
"""

_score = 0


def draw(screen: Surface):
    """
    Draw the score on the bottom right of the screen.
    """
    #
    # Because the font never changes, it really only needs to be initialized
    # once. Once done, save it as an attribute on the function itself to
    # essentially make it a static variable for the draw function.
    #
    if not hasattr(draw, "font"):
        draw.font = pygame.font.SysFont(_FONT_NAME, _FONT_SIZE, bold=True)

    text = draw.font.render(f"{_score:,}", True, _TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.bottomright = (screen.get_width() - text_rect.height, screen.get_height() - text_rect.height)
    screen.blit(text, text_rect)


def _update(base_value: int, ball_velocity: Vector2):
    """
    Add points to the score for various game events. This function is
    intended to be used internally and is called by the other scoring event
    functions such as brick_destroyed() or screen_cleared().

    This code makes sure that the score goes up by at least 1 point when
    called regardless of how the math works out.

    :param base_value: The base value for the event.
    :param ball_velocity: The Vector2 velocity of the ball at the time the
                           event. The faster the ball, the higher the score.
    """
    global _score

    #
    # Use magnitude_squared() instead of magnitude() because it is more
    # efficient and will be magnified more anyway.
    #
    _score += max(1, int(_SPEED_FACTOR * ball_velocity.magnitude_squared() * base_value))


def brick_destroyed(base_brick_value: int, ball_velocity: Vector2):
    """
    Add points to the score for destroying a brick.

    :param base_brick_value: The base value for a brick. Typically, this is
                                1 for normal bricks, qnd 5 or 10 for "special"
                                bricks.
    :param ball_velocity: The Vector2 velocity of the ball at the time the
                            brick was destroyed. The faster the ball, the
                            higher the score.
    """
    _update(base_brick_value, ball_velocity)


def screen_cleared(ball_velocity: Vector2):
    """
    Add points to the score for clearing the screen. The points are adjusted
    based on the speed of the ball at the time the screen is cleared.

    :param ball_velocity:
    """
    _update(1000, ball_velocity)
