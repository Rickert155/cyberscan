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
from .core import greeting, CoreSetting, divide_line

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
        sys.exit(CyberHelp().help_wp_plagins(doc=__doc__))
    except requests.exceptions.ConnectionError:
        sys.exit(f"{RED}Проверь правильность адреса: {url}{RESET}")

def full_url_plugin(url:str, plugin:str) -> str:
    """Возвращает полный url до readme.md"""
    if url[-1] == "/":url = url[:-1]
    full_url = f"{url}/wp-content/plugins/{plugin}/readme.txt"
    return full_url

def full_list_plugins() -> list[str]:
    "Возвращает полный список доступных для проверки плагинов"
    list_plugins = []
    plugins_file = CoreSetting().get_settings()["path_default_wp_plugin"]
    with open(plugins_file, "r") as file:
        for line in file.readlines():
            list_plugins.append(line.strip())
    return list_plugins

def parser_txt(response:str) -> dict[str]:
    """Парсер readme.txt, возвращает dict с именем и версией"""
    
    data = {
            "plugin_name":None,
            "plugin_version":None
            }
    
    readme = response.text
    all_line_readme = readme.split("\n")
    for count_line, line in enumerate(all_line_readme):
        if count_line == 0:
            plugin_name = line.replace("=", "").replace("\r", "").strip()
            data["plugin_name"] = plugin_name
        if "Stable tag: " in line:
            plugin_version = line.split("Stable tag: ")[1].strip()
            data["plugin_version"] = plugin_version

    return data

def scan_list_plugin(url:str) -> None:
    headers = Headers()
    list_plugins = full_list_plugins()
    number_valid_plugin = 0
    count_plugin = 0
    for plugin in list_plugins:
        count_plugin+=1
        full_url = full_url_plugin(url=url, plugin=plugin)
        #print(full_url)
        header = headers.create_headers()
        response = requests.get(full_url, headers=header)
        if response.status_code == 200:
            number_valid_plugin+=1
            data = parser_txt(response=response)
            plugin_name = data["plugin_name"]
            plugin_version = data["plugin_version"]
            print(
                    f"|{divide_line()}\n"
                    f"| [{number_valid_plugin}]\n"
                    f"| {GREEN}Plugin:     {BOLD}{plugin_name}{RESET}\n"
                    f"| {GREEN}Version:    {BOLD}{plugin_version}{RESET}"
                    )
        print(f"[{count_plugin}/{len(list_plugins)}]  {plugin}", end="\r")


def scanWordPressPlugins(url:str):
    wp_status = check_wordpress(url=url)
    
    if wp_status[0] == True:
        scan_list_plugin(url=url)

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
