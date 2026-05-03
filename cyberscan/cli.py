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
from cyberscan.social.cyberwarnuser import cyberwarnuser
from cyberscan.fuzz.fuzz_subdomain import fuzz_subdomains
from cyberscan.fuzz.fuzz_dirs import fuzz_dirs
from cyberscan.fuzz.get_links import get_links

def show_menu() -> str:
    text = f"""\
    |{divide_line()}
    |   {BOLD}{__project__}{RESET}
    |
    |   {GREEN}[1] {BOLD}Поиск поддоменов: fuzz_subdomain{RESET}
    |   {GREEN}[2] {BOLD}Поиск файлов/директорий: fuzz_dirs{RESET}
    |   {GREEN}[3] {BOLD}Поиск ссылок на странице: get_links{RESET}
    |
    |   {BLUE}Social{RESET}
    |   {GREEN}[4] {BOLD}Поиск по username: username(в процессе разработки){RESET}
    |
    |   {BLUE}CMS{RESET}
    |   {GREEN}[5] {BOLD}Сканер плагинов WordPress: wp-plugins{RESET}
    |   {GREEN}[6] {BOLD}Определить версию WordPress: wp-version{RESET}
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
            
            if "fuzz_subdomain" in item or item == "1":
                """Search subdomains"""
                fuzz_subdomains(
                        url=input("| URL: ").strip(),
                        wordlist_path=input("| Wordlist(path): ").strip()
                        )
            
            elif "fuzz_dirs" in item or item == "2":
                """Search subdomains"""
                fuzz_dirs(
                        url=input("| URL: ").strip(),
                        wordlist_path=input("| Wordlist(path): ").strip()
                        )
            elif "get_links" in item or item == "3":
                """Get all links by page"""
                get_links(url=input("| URL: ").strip())
            
            elif "username" in item or item == "4":
                """Search by username"""
                cyberwarnuser(username=input("| Username: ").strip())
            
            elif "wp-plugins" in item or item == "5":
                """WP plugins"""
                scanWordPressPlugins(url=input("| URL: ").strip())
            
            elif "wp-version" in item or item == "6":
                """WP version"""
                scanWordPressVersion(url=input("| URL: ").strip())
            
        elif len(params) == 3 and "fuzz_subdomain" in params[0] \
                and ("https://" in params[1] or "http://" in params[1]):
            url = params[1]
            wordlist = params[2]
            fuzz_subdomains(url=url, wordlist_path=wordlist)

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
        elif len(params) == 2 and "get_links" in params[0] \
                and ("http://" in params[1] or "https://" in params[1]):
            url = params[1]
            get_links(url=url)

        else:
            sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")
    except ValueError as err:
        sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except IndexError:
        sys.exit(CyberHelp().help_main_menu(doc=__doc__))
