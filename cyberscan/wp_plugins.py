"""
Модуль: Сканер плагинов WordPress
Пример использования:
    python3 -m cyberscan.wp_plugins --url="https://example.com"
    python3 -m cyberscan.wp_plugins url="https://example.com"
"""
import requests
import sys
from .header import Headers
from .helper import CyberHelp
from .colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from .core import greeting

def check_wordpress(url:str) -> bool:
    """Проверяем, на WordPress сайт или нет"""
    headers = Headers().create_headers()

    status_ok = [200, 403, 301, 302, 303, 308]

    try:
        wp_admin_url = f"{url}/wp-admin/"
        response = requests.get(url=wp_admin_url, headers=headers)
        status_code = response.status_code
        if status_code in status_ok:
            return True, status_code
        else:
            return False, status_code
    except requests.exceptions.InvalidURL:
        print(CyberHelp().help_wp_plagins(doc=__doc__))
    except requests.exceptions.ConnectionError:
        print(f"{RED}Проверь правильность адреса: {url}{RESET}")

def scanWordPressPlugins(url:str):
    wp_status = check_wordpress(url=url)
    
    if wp_status[0] == True:
        print(f"WordPress, status: {wp_status[1]}")
            

    elif wp_status[0] != True and wp_status[1] >= 500:
        print(
                f"| {YELLOW}{url} Проблемы на стороне сервера: "
                f"{wp_status[1]}{RESET}"
                )
    else:
        print(
                f"| {YELLOW}{url} Сайт не на WordPress, "
                f"status: {wp_status[1]}{RESET}"
                )

if __name__ == "__main__":
    print(greeting())
    params = sys.argv[1:]
    if len(params) != 0 and "url=" in params[0] \
            and ("http://" in params[0] or "https://" in params[0]) \
            and len(params[0].split("url=")[1]) > 0:
        url = params[0].split("url=")[1]
        if url[-1] == "/": url = url[:-1]
        scanWordPressPlugins(url=url)
    else:
        print(CyberHelp().help_wp_plagins(doc=__doc__))
