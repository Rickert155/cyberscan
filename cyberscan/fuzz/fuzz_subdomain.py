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
from concurrent.futures import ThreadPoolExecutor
from threading import Lock


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


COUNT_SUBDOMAINS = 0
COUNT_FIND_SUBDOMAINS = 0
LEN_LIST_SUBDOMAINS = 0
RESULT_FILE = ""
count_subdomains_lock = Lock()
count_find_subdomain_lock = Lock()
update_txt_lock = Lock()

def check_subdomain(subdomain:str) -> list[bool, str]:
    global COUNT_SUBDOMAINS, COUNT_FIND_SUBDOMAINS
    with count_subdomains_lock:
        COUNT_SUBDOMAINS+=1

    if COUNT_SUBDOMAINS % 100 == 0 or COUNT_SUBDOMAINS == LEN_LIST_SUBDOMAINS:
        print(
                f"{GREEN}| Progress: "
                f"[{COUNT_SUBDOMAINS}/{LEN_LIST_SUBDOMAINS}]{RESET}"
                )
    try:
        headers = Headers().create_headers()
        response = requests.get(subdomain, headers=headers)
        status_code = response.status_code
        server_headers = response.headers
        
        with count_find_subdomain_lock:
            COUNT_FIND_SUBDOMAINS+=1
        
        text_headers = ""
        for key, value in server_headers.items():
            text_headers+=f"{key}: {value}\n"
        text_headers = text_headers.strip()
        print(
                f"{GREEN}| [{COUNT_FIND_SUBDOMAINS}] {subdomain}: "
                f"{RESET}{YELLOW}{status_code}{RESET}"
                )
        with update_txt_lock:
            with open(RESULT_FILE, "a") as file:
                file.write(
                        f"{subdomain} {status_code}\n\n"
                        f"{text_headers}\n"
                        f"{'-'*50}\n"
                        )
    except requests.exceptions.ConnectionError:
        pass
    except Exception as err:
        print(
                f"{RED}| {subdomain}: {err}{RESET}"
                )


def fuzz_subdomains(args:dict[str]) -> None:
    global LEN_LIST_SUBDOMAINS, RESULT_FILE
    url = args["--url"]
    wordlist_path = args["--wordlist"]
    workers = args["--workers"]
    try:
        workers = int(workers)
    except ValueError:
        sys.exit(f"| {RED}Значение workers должно быть числовым{RESET}")
    template = args["template"]
    RESULT_FILE = f'{url.split("//")[1].split("/")[0]}.subdomains.txt'
    if os.path.exists(RESULT_FILE):
        os.remove(RESULT_FILE)
    if not url.startswith("https://") and not url.startswith("http://"):
        sys.exit(f"| {RED}Пример использования: {template}{RESET}")
    
    """Основной компонент"""
    if not os.path.exists(wordlist_path):
        sys.exit(f"{BOLD}{RED}wordlist not found: {wordlist_path}{RESET}")
    if url[-1] == "/":url = url[:-1]

    wordlist = get_wordlist(wordlist_path=wordlist_path)
    path_file = url.split("://")[1]+"_fuzz_subdomains.txt"
    if os.path.exists(path_file):os.remove(path_file)

    list_subdomains = []
    for count, word in enumerate(wordlist, start=1):
        protocol, domain = url.split("://")
        full_domain = f"{protocol}://{word}.{domain}"
        list_subdomains.append(full_domain)
    
    LEN_LIST_SUBDOMAINS = len(list_subdomains)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        result = list(executor.map(
            check_subdomain,
            list_subdomains
            ))
