"""
Модуль: CLI меню
При запуске инструмента без параметров будет показано меню. В таком случае
можно выбрать номер модуля или его альтернативное название(указывается 
после двоеточие). Пример использования для сканирования плагинов WordPress:
|---------------------------------------------
|   CyberScan
|   [1] Сканер плагинов WordPress: wp-plugins
|   [2] Определить CMS: cms
| >>> wp-plugins

или

|---------------------------------------------
|   CyberScan
|   [1] Сканер плагинов WordPress: wp-plugins
|   [2] Определить CMS
| >>> 1
"""
import textwrap
import sys
from .core import init, divide_line
from . import __project__
from .colors import RED, RESET, BLUE, GREEN, BOLD
from .wp_plugins import scanWordPressPlugins
from .helper import CyberHelp

def show_menu() -> str:
    text = f"""\
    |{divide_line()}
    |   {BOLD}{__project__}{RESET}
    |   {GREEN}[1] {BOLD}Сканер плагинов WordPress: wp-plugins{RESET}
    |   {GREEN}[2] {BOLD}Определить CMS: cms{RESET}
    """
    text = textwrap.dedent(text)
    return text

def main():
    try:
        init()
    
        params = sys.argv[1:]
        if len(params) == 0:
            item = input(f"{show_menu()}| >>> ")
            if item == "wp-plugins" or int(item) == 1:
                scanWordPressPlugins(url=input("URL: ").strip())
        elif len(params) > 1 and "wp-plugins" in params[0] \
                and "https://" in params[1] or "http://" in params[1]:
            url = params[1]
            scanWordPressPlugins(url=url)
        else:
            sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")
    except ValueError as err:
        sys.exit(CyberHelp().help_main_menu(doc=__doc__))
