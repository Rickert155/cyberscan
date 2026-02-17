import textwrap
from .colors import RED, RESET, BOLD, GREEN
from . import (
        __author__, 
        __version__, 
        __project__, 
        __authorurl__,
        __license__
        )

def greeting():
    greet_text = f"""\
    {BOLD}author:       {__author__}{RESET}\t{GREEN}{__authorurl__}{RESET}
    {BOLD}project:      {__project__}{RESET}\t{GREEN}{__license__}{RESET}      
    {BOLD}version:      {__version__}{RESET} \
    """
    greet_text = textwrap.dedent(greet_text)
    return greet_text

