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
from cyberscan.core.core import init, divide_line
from __init__ import __project__
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD
from cyberscan.cms.wp_plugins import scanWordPressPlugins
from cyberscan.cms.wp_version import scanWordPressVersion
from cyberscan.core.helper import CyberHelp

def show_menu() -> str:
    text = f"""\
    |{divide_line()}
    |   {BOLD}{__project__}{RESET}
    |   {GREEN}[1] {BOLD}Сканер плагинов WordPress: wp-plugins{RESET}
    |   {GREEN}[2] {BOLD}Определить версию WordPress: wp-version{RESET}
    |   {GREEN}[3] {BOLD}Определить CMS: cms{RESET}
    """
    text = textwrap.dedent(text)
    return text

def main():
    try:
        init()
    
        params = sys.argv[1:]
        if len(params) == 0:
            """Работа через меню"""
            item = input(f"{show_menu()}| >>> ").strip()
            if "wp-plugins" in item or item == "1":
                scanWordPressPlugins(url=input("| URL: ").strip())
            elif "wp-version" in item or item == "2":
                scanWordPressVersion(url=input("| URL: ").strip())
        elif len(params) == 2 and "wp-plugins" in params[0] \
                and ("https://" in params[1] or "http://" in params[1]):
            """Работа с параметрами"""
            url = params[1]
            scanWordPressPlugins(url=url)
        elif len(params) == 2 and "wp-version" in params[0] \
                and ("https://" in params[1] or "http://" in params[1]):
            """Работа с параметрами"""
            url = params[1]
            scanWordPressVersion(url=url)
        else:
            sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")
    except ValueError as err:
        sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except IndexError:
        sys.exit(CyberHelp().help_main_menu(doc=__doc__))
