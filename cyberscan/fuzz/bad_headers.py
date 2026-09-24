import requests
import os
import sys
from cyberscan.core.colors import RED, RESET, GREEN, BOLD
from cyberscan.core.header import Headers
from cyberscan.core.core import get_proxy, divide_line

def get_headers(file_name:str, type_file:str) -> dict[str] | list[str]:
    """
    type_file - может быть два вида файлов: source и payloads
    source - стартовый файл с заголовками
    payloads - файл с нагрузкой
    """
    if not os.path.exists(file_name):
        sys.exit(
                f"| {RED}Не обнаружен файл с заголовками: {BOLD}{file_name}{RESET}"
                )
    if type_file == "source":
        headers = {}
    elif type_file == "payloads":
        headers = []
    else:
        sys.exit(get_headers.__doc__)

    with open(file_name, "r") as file:
        count_line = 0
        for line in file.readlines():
            count_line+=1
            line = line.strip()
            try:
                key, value = line.split(":", 1)
                key, value = key.strip(), value.strip()
                
                if type_file == "source":
                    headers[key] = value
                elif type_file == "payloads":
                    data = {"key":key, "value":value}
                    headers.append(data)
                else:
                    sys.exit(get_headers.__doc__)
            
            except ValueError:
                sys.exit(
                        f"| {RED}{file_name} line[{count_line}] '{line}'{RESET}\n"
                        f"| {RED}Необходимо передать ключ и "
                        f"значение через двоеточие{RESET}"
                        )
    return headers

HARD_SERVERS = ["cloudflare"]
RESULT_FILE = ""

def recording_result(text:str):
    with open(RESULT_FILE, "a+") as file:
        file.write(f"{text}\n\n")

def check_response(url:str, payload:dict[str], headers:dict[str]) -> None:
    proxy = get_proxy()
    try:
        user_key, user_value = payload["key"], payload["value"]
        headers[user_key] = user_value
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        status_code = response.status_code
        content_length = len(response.content)
        response_headers = response.headers
            
        response_server = response_headers.get("server")
        x_powered_by_server = response_headers.get("x-powered-by")
            
        response_headers_text = (
                f"{status_code} {url}\n"
                f"Content length: {content_length}\n"
                f"{user_key}: {user_value}\n\n"
                )
        for key in response_headers:
            text = f"{key}: {response_headers[key]}\n"
            response_headers_text+=text
        
        output_text = (
                f"| {GREEN}Status code{RESET}: {status_code}\n"
                f"| {GREEN}Content length{RESET}: "
                f"{BOLD}{content_length}{RESET}\n"
                )
        if response_server:
            output_text+=f"| {GREEN}Server{RESET}: {response_server}\n"
            if response_server in HARD_SERVERS:
                output_text = output_text.replace(
                        response_server, f"{RED}{response_server}{RESET}"
                        )
        if x_powered_by_server:
            output_text+=(
                    f"| {GREEN}X-Powered-By{RESET}: "
                    f"{x_powered_by_server}\n"
                    )
        output_text+=(
                f"| {divide_line()[:-1]}"
                )
        print(output_text)
        #print(response.headers)
        recording_result(text=response_headers_text)
    except Exception as err:
        print(f"| {RED}{err}{RESET}")

def bad_headers(args:dict[str]):
    global RESULT_FILE
    url = args["--url"]
    
    # Исходный файл с заголовками
    source_headers= args["--headers"]
    # Пользовательские заголовки
    users_payloads = args["--payloads"]
    
    template = args["template"]

    if not url.startswith("https://") and not url.startswith("http://"):
        sys.exit(f"| {RED}Пример использования: {template}{RESET}")
    
    source_headers = get_headers(file_name=source_headers, type_file="source")
    users_payloads = get_headers(file_name=users_payloads, type_file="payloads")

    RESULT_FILE = url.split("://")[1]
    if "/" in RESULT_FILE:RESULT_FILE = RESULT_FILE.split("/")[0]
    RESULT_FILE = f"{RESULT_FILE}.bad-headers.txt"
    if os.path.exists(RESULT_FILE):os.remove(RESULT_FILE)
    
    # Перебор пользовательских payloads
    for user_payloads in users_payloads:
        user_key, user_value = user_payloads["key"], user_payloads["value"]
        # Добавляем payload в исходный файл с заголовками
        headers = source_headers.copy()
        payload = {"key":user_key, "value":user_value}
        user_agent = headers.get("User-Agent")
        if user_agent == None:
            headers["User-Agent"] = Headers().create_headers()["User-Agent"]
        check_response(url=url, payload=payload, headers=headers)



