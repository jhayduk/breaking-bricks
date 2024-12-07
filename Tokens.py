import pygame
from pygame import Surface
from score import FONT_SIZE as SCORE_FONT_SIZE


class Tokens:
    """
    Tokens are the equivalent of lives or hearts. The player starts out with a
    certain number of them, and when they run out, the game is over.

    The tokens are rendered in the bottom left corner of the screen after any
    background is drawn, and before any game elements. This way, if the ball
    happens to travel past them, the ball will be displayed on top of the tokens,
    as if it is passing over them.

    The current token image is from the Nintendo 64 version of Mario Party as
    downloaded from spriters-resource.com at:
    https://www.spriters-resource.com/nintendo_64/marioparty/sheet/147290/
    and then cropped to contain just the token.
    """
    _TOKEN_IMAGE_FILE = "./images/token.png"
    _STARTING_NUM_TOKENS = 3
    _MAX_TOKENS_BEFORE_STACKING = 10
    _image = None

    num_tokens = _STARTING_NUM_TOKENS
    """
    This is the current number of tokens the player has.

    This is typically read to see if the game should be over because the
    player has no tokens left, but is available so that it can be used for
    other purposes if desired (e.g. to change the background music when the
    tokens are getting low).
    
    This should be READ ONLY and never written to. Use the add() and lose()
    class methods to adjust the count.
    """

    @classmethod
    def draw(cls, screen: Surface):
        """
        Draw the current set of tokens in the bottom left of the screen.
        """
        #
        # Load the image and perform any calculations that will never change
        # only once.
        #
        if cls._image is None:
            cls.image = pygame.image.load(cls._TOKEN_IMAGE_FILE).convert_alpha()
            cls.image = pygame.transform.smoothscale(cls.image, (SCORE_FONT_SIZE, SCORE_FONT_SIZE))
            cls.image_rect = cls.image.get_rect()
            cls.image_rect.y = screen.get_height() - (2 * cls.image_rect.height)
            cls.max_space_for_all_tokens = cls._MAX_TOKENS_BEFORE_STACKING * cls.image_rect.width

        if cls.num_tokens > 0:
            x_offset_between_tokens = min(cls.max_space_for_all_tokens / cls.num_tokens, cls.image_rect.width)

            for token_index in range(cls.num_tokens):
                cls.image_rect.x = cls.image_rect.width + (token_index * x_offset_between_tokens)
                screen.blit(cls.image, cls.image_rect)

    @classmethod
    def add(cls, tokens_to_add: int = 1):
        """
        Add tokens to the total.

        This is expected to be called anytime the player gains tokens. This
        generally happens when a level is cleared, or if a "token" brick is
        destroyed. This will almost always increase the number of tokens
        by 1, but the tokens_to_add parameter can be used if a larger amount
        is appropriate.

        :param int tokens_to_add: The number of tokens to add. Defaults to 1.
        """
        cls.num_tokens += tokens_to_add

    @classmethod
    def lose(cls, tokens_to_remove: int = 1):
        """
        Remove tokens from the total.

        This is expected to be called anytime the player loses tokens. This
        generally happens when the ball falls off the bottom of the screen.
        This will almost always decrease the number of tokens by 1, but the
        tokens_to_remove parameter can be used if a larger amount is appropriate.

        :param int tokens_to_remove: The number of tokens to remove. Defaults to 1.
        """
        cls.num_tokens = max(0, cls.num_tokens - tokens_to_remove)
