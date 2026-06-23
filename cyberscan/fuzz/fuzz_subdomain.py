"""
Модуль: Сканнер поддоменов
"""
import json
import os
import requests
import sys
from cyberscan.core.header import Headers
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.core.core import CoreSetting, divide_line 


def get_wordlist(wordlist_path:str) -> set:
    """Получаем список wordlist"""
    wordlist = set()
    try:
        with open(wordlist_path, "r") as file:
            for line in file.readlines():
                word = line.strip()
                if len(word) > 0:
                    if word[0] == ".":word = word[1:]
                    wordlist.add(word)
        return wordlist
    except Exception as err:
        sys.exit(f"{RED}{err}{RESET}")

def recording_subdomain(
        subdomain:str,
        response:str,
        headers:str,
        path_file:str
        ) -> None:
    divide_line = "-"*10
    with open(path_file, "a+") as file:
        file.write(
                f"{subdomain} {response}\n"
                f"{headers.strip()}\n"
                f"{divide_line}\n\n"
                )

def check_subdomain(subdomain:str) -> list[bool, str]:
    status_subdomain = True 
    try:
        headers = Headers().create_headers()
        response = requests.get(subdomain, headers=headers)
        status_code = response.status_code
        return status_subdomain, status_code, response.headers
    except requests.exceptions.ConnectionError:
        status_subdomain = False
        return status_subdomain, "Connection error"
    except Exception as err:
        status_subdomain = False
        return status_subdomain, err


def fuzz_subdomains(args:dict[str]) -> None:
    url = args["--url"]
    wordlist_path = args["--wordlist"]
    template = args["template"]
    if not url.startswith("https://") and not url.startswith("http://"):
        sys.exit(f"| {RED}Пример использования: {template}{RESET}")
    
    """Основной компонент"""
    if not os.path.exists(wordlist_path):
        sys.exit(f"{BOLD}{RED}wordlist not found: {wordlist_path}{RESET}")
    if url[-1] == "/":url = url[:-1]

    wordlist = get_wordlist(wordlist_path=wordlist_path)
    path_file = url.split("://")[1]+"_fuzz_subdomains.txt"
    if os.path.exists(path_file):os.remove(path_file)

    print(f"| Длина списка: {len(wordlist)}")

    for count, word in enumerate(wordlist, start=1):
        protocol, domain = url.split("://")
        full_domain = f"{protocol}://{word}.{domain}"
        result = check_subdomain(subdomain=full_domain)
        output_text = f"| [{count}/{len(wordlist)}] {full_domain}"
        if result[0]:
            server_headers = ""
            for key, value in result[-1].items():
                server_headers+=f"{key}: {value}\n"
            recording_subdomain(
                    subdomain=full_domain,
                    response=result[1],
                    headers=server_headers,
                    path_file=path_file
                    )
            output_text = f"{GREEN}{output_text}{RESET} {result[:-1]}"
        else:
            output_text = f"{RED}{output_text} {result}{RESET}"
        print(output_text)
