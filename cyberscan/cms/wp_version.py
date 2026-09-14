""""
Модуль: сканер версии WordPress
"""
import sys
import requests
from cyberscan.core.header import Headers
from cyberscan.core.core import greeting, divide_line, get_proxy
from cyberscan.core.colors import GREEN, RESET, BOLD, RED
from bs4 import BeautifulSoup


def parser_version(url:str) -> str:
    version = None
    list_version = set()

    try:
        headers = Headers().create_headers()
        headers["Accept-Encoding"] = "gzip, deflate"
        full_url = f"{url}/wp-admin/about.php"
        proxy = get_proxy()
        response = requests.get(full_url, headers=headers, proxies=proxy)
        status_code = response.status_code
        if status_code == 200:
            bs = BeautifulSoup(response.text, "lxml")
            for script in bs.find_all("script"):
                wp_url = script.get("src")
                if wp_url != None and "/wp-admin/" in wp_url:
                    if "?ver=" in wp_url:
                        version = wp_url.split("?ver=")[1]
                        list_version.add(version)

            list_version = list(list_version)
            if len(list_version) == 1:
                return list_version[0]
            elif len(list_version) > 1:
                return f"Возможные версии WordPress: {list_version}"
            else:
                return f"Не удалось узнать версию WordPress"

        else:
            return f"Status code: {status_code}"
    except requests.exceptions.ConnectionError:
        return f"Не удалось сделать запрос к сайту"
    except Exception as error:
        return f"Error: {error}"

def scanWordPressVersion(args:dict[str]) -> None:
    url = args["--url"]
    template = args["template"]
    if not url.startswith("https://") and not url.startswith("http://"):
        sys.exit(f"| {RED}Пример использования: {template}{RESET}")
    version = parser_version(url=url)
    print(
            f"| {GREEN}WordPress version:\t{BOLD}{version}{RESET}"
            )

