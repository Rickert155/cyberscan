"""
Модуль: CLI меню
"""
import textwrap
import sys
from cyberscan.core.core import init, divide_line, greeting
from __init__ import __project__
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.cms.wp_plugins import scanWordPressPlugins
from cyberscan.cms.wp_version import scanWordPressVersion
from cyberscan.social.cyberwarnuser import cyberwarnuser
from cyberscan.fuzz.fuzz_subdomain import fuzz_subdomains
from cyberscan.fuzz.fuzz_dirs import fuzz_dirs
from cyberscan.fuzz.get_links import get_links
from cyberscan.fuzz.get_comments import get_comments

COMMANDS = {
        "fuzz_subdomains":{
            "name":"Сканер поддоменов",
            "module":fuzz_subdomains,
            "args":["--url=", "--wordlist="],
            "example_url":"http://example.com",
            "example_wordlist":"data/wordlist/web/subdomains.txt",
            "template":(
                "python3 -m cyberscan fuzz_subdomains "
                "--url=https://example.com --wordlist=data/wordlist/web/subdomains.txt"
                )
            },
        "fuzz_dirs":{
            "name":"Сканер директорий",
            "module":fuzz_dirs,
            "args":["--url=", "--wordlist="],
            "example_url":"http://example.com",
            "example_wordlist":"data/wordlist/web/dir.txt",
            "template":(
                "python3 -m cyberscan fuzz_dirs "
                "--url=https://example.com --wordlist=data/wordlist/web/dir_959.txt"
                )
            },
        "get_links":{
            "name":"Сборщик ссылок",
            "module":get_links,
            "args":["--url="],
            "example_url":"http://example.com",
            "template":"python3 -m cyberscan get_links --url=https://example.com"
            },
        "get_comments":{
            "name":"Сборщик комментариев",
            "module":get_comments,
            "args":["--url="],
            "example_url":"http://example.com",
            "template":"python3 -m cyberscan get_comments --url=https://example.com"
            },
        "wp-plugins":{
            "name":"Сканер плагинов WordPress",
            "module":scanWordPressPlugins,
            "args":["--url="],
            "example_url":"http://example.com",
            "template":"python3 -m cyberscan wp-plugins --url=https://example.com"
            },
        "wp-version":{
            "name":"Сканер версии WordPress",
            "module":scanWordPressVersion,
            "args":["--url="],
            "example_url":"http://example.com",
            "template":"python3 -m cyberscan wp-version --url=https://example.com"
            }
        }

def show_menu(helper:bool=False) -> str:
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
        if helper:
            commands_text+=f"| {BLUE}{COMMANDS[command]["template"]}{RESET}\n"
    commands_text = commands_text.strip()
    return commands_text 

def main():
    print(f"{greeting()}\n|{divide_line()}")
    init()
    params = sys.argv[1:]
    if len(params) == 0:
        print(show_menu())
    
    elif len(params) > 0 and "--help" in params[0]:
        print(show_menu(helper=True))

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
                    key, value = user_commands.split("=", 1)
                    data[key] = value
                    data["template"] = COMMANDS[params[0]]["template"]
                except ValueError:
                    sys.exit(
                            f"| {RED}Необходимо корректно передать аргументы:{RESET} "
                            f"{COMMANDS[params[0]]["args"]}\n"
                            f"| {BLUE}{COMMANDS[params[0]]["template"]}{RESET}"
                            )
                if key+"=" not in COMMANDS[params[0]]["args"]:
                    sys.exit(
                            f"| {RED}Необходимо передать аргументы: {RESET}"
                            f"{COMMANDS[params[0]]["args"]}\n"
                            f"| {COMMANDS[params[0]]["template"]}"
                            )
            COMMANDS[params[0]]["module"](args=data)
        else:
            sys.exit(
                    f"| {RED}Необходимо передать аргументы: {RESET}"
                    f"{COMMANDS[params[0]]["args"]}\n"
                    f"| {COMMANDS[params[0]]["template"]}"
                    )
