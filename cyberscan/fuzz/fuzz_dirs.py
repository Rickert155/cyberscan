"""
Модуль: Сканнер директорий 
Пример исопользования:
    python3 -m cyberscan.fuzz.fuzz_dirs \\ 
            --url="https://example.com" --wordlist="path/wordlist.txt"
    python3 -m cyberscan.fuzz.fuzz_dirs \\
            url="https://example.com" wordlist="path/wordlist.txt"
"""
import os
import json
import requests
import sys
from cyberscan.core.header import Headers
from cyberscan.core.helper import CyberHelp
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.core.core import greeting, CoreSetting, divide_line

WARNING_WORDS = [
        "robots.txt", 
        ".env",
        ".htaccess"
        ]

def get_wordlist(wordlist_path:str):
    wordlist = set()
    try:
        with open(wordlist_path, "r") as file:
            for line in file.readlines():
                url = line.strip()
                if len(url) > 0:wordlist.add(url)
        return wordlist
    except Exception as err:
        sys.exit(f"{RED}{err}{RESET}")

def recording_result(
        url:str, 
        status_code:str, 
        server_headers:str,
        path_file:str,
        word:str,
        text:str=None
        ):
    divide_line = "="*20
    server_headers = server_headers.strip()
    recording_text = f"{url} {status_code}\n\n{server_headers}\n\n"

    with open(path_file, "a+") as file:
        if text != None and word in WARNING_WORDS and status_code == 200:
            recording_text+=f"{text}\n{divide_line}\n\n"
            file.write(recording_text)
        else:
            recording_text+=f"{divide_line}\n\n"
            file.write(recording_text)


def check_url(url:str) -> list[bool, dict|str]:
    status_url = False
    try:
        headers = Headers().create_headers()
        response = requests.get(url, headers=headers)
        
        status_code = response.status_code
        server_headers = response.headers
        page_text = response.text
        if status_code != 404:status_url = True
        data = {
                "status_url":status_url,
                "server":server_headers, 
                "status_code":status_code,
                "text":page_text
                }
        return status_url, data
    except requests.exceptions.ConnectionError:
        return status_url, "Connection error"
    except Exception as err:
        return status_url, err

def fuzz_dirs(url:str, wordlist_path:str):
    if not os.path.exists(wordlist_path):
        sys.exit(f"{BOLD}{RED}wordlist not found: {wordlist_path}{RESET}")
    if "://" not in url:
        sys.exit(f"{BOLD}{RED}url not found: {url}{RESET}")
    if url[-1] == "/":url = url[:-1]

    wordlist = get_wordlist(wordlist_path=wordlist_path)
    path_file = url.split("://")[1]+"_fuzz_url.txt"
    if os.path.exists(path_file):os.remove(path_file)
    

    for count, word in enumerate(wordlist, start=1):
        full_url = f"{url}/{word}"
        result, data = check_url(url=full_url)
        output_text = f"| [{count}/{len(wordlist)}] {full_url}"

        server_info = ""
        for key, value in data["server"].items():
            server_info+=f"{key}: {value}\n"
        
        if result:
            output_text = f"{GREEN}{output_text} {data['status_code']}{RESET}"
            recording_result(
                url=full_url,
                server_headers=server_info,
                path_file=path_file,
                word=word,
                status_code=data["status_code"],
                text=data["text"],
                )

        else:
            output_text = f"{RED}{output_text} {result} {data['status_code']}{RESET}"

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
            fuzz_dirs(url=url, wordlist_path=wordlist)
    
        else:
            sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")
