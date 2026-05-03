"""
Модуль: get links

Пример использования:
    python3 -m cyberscan --url=http://example.com
    python3 -m cyberscan.fuzz.get_links --url=http://example.com

Примечание:
    необходимо определить протокол [http/https]
"""
import os
import requests
import sys
from cyberscan.core.header import Headers
from cyberscan.core.helper import CyberHelp
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.core.core import greeting
from bs4 import BeautifulSoup

def recording_urls(file_name:str, urls:[]=None) -> None:
    with open(file_name, "w") as file:
        for url in urls:
            file.write(f"{url}\n")

def extract_links(response:str, url:str) -> list[str] | None:
    list_links = []
    try:
        bs = BeautifulSoup(response, "lxml")
        all_links = bs.find_all(["a", "link"])
        if len(all_links) > 0:
            for link in all_links:
                if link != None:
                    link = link.attrs["href"]
                    if link[0] == "/":link = link[1:]
                    if "http" not in link and "://" not in link:
                        link = f"{url}/{link}"
                    if link not in list_links:
                        list_links.append(link)
        return list_links
    except Exception as err:
        print(f"{RED}ERROR Extraction: {err}{RESET}")
        return list_links

def get_links(url:str) -> None:
    if "http://" not in url and "https://" not in url:
        sys.exit(f"{RED}{__doc__}{RESET}")
    if url[-1] == "/":url = url[:-1]
    try:
        headers = Headers().create_headers()
        headers["Host"] = url.split("://")[1]

        response = requests.get(url, headers=headers)
        status_code = response.status_code
        if response.status_code == 200:
            links = extract_links(response=response.text, url=url)
            if len(links) > 0:
                file_name = f"{url.split("://")[1]}_links.txt"
                recording_urls(urls=links, file_name=file_name)
                for count, link in enumerate(links, start=1):
                    print(f"| [{count}] {GREEN}{link}{RESET}")
            else:
                sys.exit(f"| {RED}Ссылки не обнаружены!{RESET}")

    except KeyboardInterrupt:
        sys.exit(f"| {RED}\nExit...{RESET}")
    except requests.exceptions.ConnectionError:
        sys.exit(f"| {RED}{url}: Connection Error{RESET}")

if __name__ == "__main__":
    print(greeting())
    params = sys.argv[1:]
    if len(params) > 0 and \
            "url=" in params[0] and \
            ("http://" in params[0] or "https://" in params[0]):
        url = params[0].split("url=")[1]
        get_links(url=url)
    else:
        sys.exit(CyberHelp().help_main_menu(doc=__doc__))
