import sys
import requests
from .header import Headers
from .helper import CyberHelp
from .core import greeting, divide_line
from .colors import GREEN, RESET, BOLD 
from bs4 import BeautifulSoup


def parser_version(url:str) -> str:
    version = None
    list_version = set()

    try:
        headers = Headers().create_headers()
        headers["Accept-Encoding"] = "gzip, deflate"
        full_url = f"{url}/wp-admin/about.php"
        response = requests.get(full_url, headers=headers)
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

def scanWordPressVersion(url:str) -> None:
    version = parser_version(url=url)
    print(
            f"|{divide_line()}\n"
            f"| {GREEN}WordPress version:\t{BOLD}{version}{RESET}"
            )

if __name__ == "__main__":
    print(greeting())
    params = sys.argv[1:]
    if len(params) != 0 and "url=" in params[0] \
            and ("http://" in params[0] or "https://" in params[0]) \
            and len(params[0].split("url=")[1]) > 0:
        url = params[0].split("url=")[1]
        if url[-1] == "/": url = url[:-1]
        scanWordPressVersion(url=url)
    else:
        print(CyberHelp().help_wp_version(doc=__doc__))

