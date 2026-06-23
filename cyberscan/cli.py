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
from cyberscan.core.core import init, divide_line, greeting
from __init__ import __project__
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.cms.wp_plugins import scanWordPressPlugins
from cyberscan.cms.wp_version import scanWordPressVersion
from cyberscan.core.helper import CyberHelp
from cyberscan.social.cyberwarnuser import cyberwarnuser
from cyberscan.fuzz.fuzz_subdomain import fuzz_subdomains
from cyberscan.fuzz.fuzz_dirs import fuzz_dirs
from cyberscan.fuzz.get_links import get_links
from cyberscan.fuzz.get_comments import get_comments

COMMANDS = {
        "fuzz_subdomains":{
            "name":"Сканер поддоменов",
            "module":fuzz_subdomains,
            "args":["--url=", "--wordlist="]
            },
        "fuzz_dirs":{
            "name":"Сканер директорий",
            "module":fuzz_dirs,
            "args":["--url=", "--wordlist="]
            },
        "get_links":{
            "name":"Сборщик ссылок",
            "module":get_links,
            "args":["--url="]
            },
        "get_comments":{
            "name":"Сборщик комментариев",
            "module":get_comments,
            "args":["--url="]
            },
        "wp-plugins":{
            "name":"Сканер плагинов WordPress",
            "module":scanWordPressPlugins,
            "args":["--url="]
            },
        "wp-version":{
            "name":"Сканер версии WordPress",
            "module":scanWordPressVersion,
            "args":["--url="]
            }
        }

def show_menu() -> str:
    commands_text = (
            f"| {BOLD}{__project__}{RESET}\n"
            )
    count_command = 0
    for command in COMMANDS:
        count_command+=1
        commands_text+=(
                f"| [{count_command}] {GREEN}{COMMANDS[command]["name"]}:"
                f" {YELLOW}{command}{RESET}\n"
                )
    commands_text = commands_text.strip()
    return commands_text 

def main():
    print(f"{greeting()}\n|{divide_line()}")
    params = sys.argv[1:]
    if len(params) == 0:
        print(show_menu())

    elif params[0] not in COMMANDS:
        commands_list = ""
        for command in COMMANDS:
            commands_list+=f"|\t{BOLD}{command}{BOLD}\n"
        commands_list = commands_list.strip()
        print(f"{RED}| Список доступных модулей:\n{commands_list}{RESET}")

    elif params[0] in COMMANDS:
        if len(COMMANDS[params[0]]["args"])+1 == len(params):
            data = {}
            for user_commands in params[1:]:
                try:
                    key, value = user_commands.split("=")
                    data[key] = value
                except ValueError:
                    sys.exit(
                            f"| Необходимо корректно передать аргументы:"
                            f"{COMMANDS[params[0]]["args"]}"
                            )
                if key+"=" not in COMMANDS[params[0]]["args"]:
                    sys.exit(
                            f"| Необходимо передать аргументы: "
                            f"{COMMANDS[params[0]]["args"]}"
                            )
            COMMANDS[params[0]]["module"](args=data)
        else:
            sys.exit(
                    f"| Необходимо передать аргументы: "
                    f"{COMMANDS[params[0]]["args"]}"
                    )
