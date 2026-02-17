import textwrap
import sys
from .core import init, divide_line
from . import __project__
from .colors import RED, RESET, BLUE, GREEN, BOLD

def show_menu() -> str:
    text = f"""\
    |{divide_line()}
    |   {BOLD}{__project__}{RESET}
    |   {GREEN}[1] {BOLD}Сканер плагинов WordPress{RESET}
    |   {GREEN}[2] {BOLD}Определить CMS{RESET}
    """
    text = textwrap.dedent(text)
    return text

def main():
    try:
        init()
    
        params = sys.argv[1:]
        if len(params) == 0:
            item = input(f"{show_menu()}| >>> ")
            print(item)
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")
