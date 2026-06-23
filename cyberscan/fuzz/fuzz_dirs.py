"""
Модуль: Сканнер директорий 
"""
import os
import json
import requests
import sys
from cyberscan.core.header import Headers
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.core.core import CoreSetting, divide_line

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

def fuzz_dirs(args:dict[str]):
    url = args["--url"]
    wordlist_path = args["--wordlist"]
    template = args["template"]
    
    if not url.startswith("https://") and not url.startswith("http://"):
        sys.exit(f"| {RED}Пример использования: {template}{RESET}")
    
    if not os.path.exists(wordlist_path):
        sys.exit(f"{BOLD}{RED}wordlist not found: {wordlist_path}{RESET}")
    
    if url[-1] == "/":url = url[:-1]

    wordlist = get_wordlist(wordlist_path=wordlist_path)
    path_file = url.split("://")[1]+"_fuzz_url.txt"
    if "/" in path_file:path_file = path_file.split("/")[0]
    if os.path.exists(path_file):os.remove(path_file)
    

    for count, word in enumerate(wordlist, start=1):
        full_url = f"{url}/{word}"
        result, data = check_url(url=full_url)
        output_text = f"| [{count}/{len(wordlist)}] {full_url}"

        
        if result:
            server_info = ""
            
            for key, value in data["server"].items():
                server_info+=f"{key}: {value}\n"
            
            output_text = (
                    f"{GREEN}{output_text} [{result} "
                    f"{data['status_code']}]{RESET}"
                    )
            recording_result(
                url=full_url,
                server_headers=server_info,
                path_file=path_file,
                word=word,
                status_code=data["status_code"],
                text=data["text"],
                )

        else:
            if type(data) == dict:
                result_text = f"[{result} {data["status_code"]}]" 
            else:
                result_text = f"[{result} {data}]"
            output_text = f"{RED}{output_text} {result_text}{RESET}"

        print(output_text)
