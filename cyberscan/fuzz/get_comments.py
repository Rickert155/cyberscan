"""
Модуль: get html comments 

Пример использования:
    python3 -m cyberscan.fuzz.get_comments --url=http://example.com

Примечание:
    необходимо определить протокол [http/https]
"""
import requests
import sys
from bs4 import BeautifulSoup
from cyberscan.core.header import Headers
from cyberscan.core.helper import CyberHelp
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.core.core import greeting

def recording_comments(url:str, comments:list=None):
    file_name = url.split("://")[1].replace("/", "--")+"_comments.txt"
    with open(file_name, "w") as file:
        text_comment = ""
        for comment in comments:
            text_comment+=f"{comment}\n"
        text_comment.strip()
        file.write(text_comment)

def get_comments(args:dict[str]):
    url = args["--url"]
    if "http://" not in url and "https://" not in url:
        sys.exit(f"{RED}{__doc__}{RESET}")
    if url[-1] == "/":url = url[:-1]
    try:
        headers = Headers().create_headers()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            list_lines = []
            source_text = response.text
            text_lines = source_text.split("\n")
            for line in text_lines:
                line = line.strip()
                if "<!--" in line:
                    list_lines.append(line)
                if "//" in line and "http" not in line:
                    list_lines.append(line)
                if line.startswith("*"):
                    if len(line.replace("*", "").strip()) != 0:
                        list_lines.append(line)

            recording_comments(url=url, comments=list_lines)
            count_line = 0 
            for line in list_lines:
                count_line+=1
                print(f"| [{count_line}] {line}")
        else:
            sys.exit(f"| {RED}Status code: {response.status_code} {url}{BOLD}")
    except Exception as err:
        print(f"| {err}")

if __name__ == "__main__":
    print(greeting())
    params = sys.argv[1:]
    if len(params) > 0 and \
            "url=" in params[0] and \
            ("http://" in params[0] or "https://" in params[0]):
        url = params[0].split("url=")[1]
        get_comments(url=url)
    else:
        sys.exit(CyberHelp().help_main_menu(doc=__doc__))
