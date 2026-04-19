"""
Модуль: Сканнер поддоменов
Пример исопользования:
    python3 -m cyberscan.fuzz.fuzz_domain \\ 
            --url="https://example.com" --wordlist="path/wordlist.txt"
    python3 -m cyberscan.fuzz.fuzz_domain \\
            url="https://example.com" wordlist="path/wordlist.txt"
"""
import os
import requests
import sys
from cyberscan.core.header import Headers
from cyberscan.core.helper import CyberHelp
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.core.core import greeting, CoreSetting, divide_line

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

def recording_subdomain(subdomain:str, path_file:str) -> None:
    with open(path_file, "a+") as file:
        file.write(f"{subdomain}\n")

def check_subdomain(subdomain:str) -> list[bool, str]:
    status_subdomain = True 
    try:
        headers = Headers().create_headers()
        response = requests.get(subdomain, headers=headers)
        status_code = response.status_code
        return status_subdomain, status_code
    except requests.exceptions.ConnectionError:
        status_subdomain = False
        return status_subdomain, "Connection error"
    except Exception as err:
        status_subdomain = False
        return status_subdomain, err


def fuzz_subdomains(url:str, wordlist_path:str) -> None:
    """Основной компонент"""
    if not os.path.exists(wordlist_path):
        sys.exit(f"{BOLD}{RED}wordlist not found: {wordlist_path}{RESET}")
    if "://" not in url:
        sys.exit(f"{BOLD}{RED}url not found: {url}{RESET}")
    if url[-1] == "/":url = url[:-1]

    wordlist = get_wordlist(wordlist_path=wordlist_path)
    path_file = url.split("://")[1]+".txt"
    if os.path.exists(path_file):os.remove(path_file)

    print(f"| Длина списка: {len(wordlist)}")

    for count, word in enumerate(wordlist, start=1):
        protocol, domain = url.split("://")
        full_domain = f"{protocol}://{word}.{domain}"
        result = check_subdomain(subdomain=full_domain)
        output_text = f"| [{count}/{len(wordlist)}] {full_domain} {result}"
        if result[0]:
            recording_subdomain(subdomain=full_domain, path_file=path_file)
            output_text = f"{GREEN}{output_text}{RESET}"
        else:
            output_text = f"{RED}{output_text}{RESET}"
        print(output_text)

if __name__ == "__main__":
    print(greeting())
    try:
        params = sys.argv[1:]
        if len(params) == 2 and ("url=" in params[0] or "--url=" in params[0]) and \
                ("http://" in params[0] or "https://" in params[0]) and \
                ("--wordlist=" in params[1] or "wordlist=" in params[1]):
            wordlist = params[1].split("wordlist=")[1]
            url = params[0].split("url=")[1]
            fuzz_subdomains(url=url, wordlist_path=wordlist)
    
        else:
            sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")

