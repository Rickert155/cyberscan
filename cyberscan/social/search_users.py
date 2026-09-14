import json
import requests
import sys
from cyberscan.core.colors import RED, RESET, GREEN, BOLD, YELLOW
from cyberscan.core.core import CoreSetting, get_proxy, divide_line
from cyberscan.core.header import Headers

from concurrent.futures import ThreadPoolExecutor
from threading import Lock

def check_user(service:dict[str], user:str):
    try:
        url = service["url"].replace("[USER]", user)
        service_name = service["name"]
        category = service["category"]
        fail_status = service["fail"]
        fail_code = service["fail_code"]
        success_text = service["success_text"]
        success_code = service["success_code"]

        headers = Headers().create_headers()
        proxy = get_proxy()
        response = requests.get(url, headers=headers, proxies=proxy)

        text_result = response.text
        status_code = response.status_code

        if status_code in fail_code and success_text not in text_result:
            print(
                    f"| user {RED}{user}: {url} {status_code}{RESET}"
                    )
        else:
            print(
                    f"| user {GREEN}{user}: {url} {status_code}{RESET}"
                    )
        
    except Exception as err:
        print(err)
        return False


def search_users(args:dict[str]):
    try:
        user = args["--user"]
        workers = args["--workers"]

        services_info = CoreSetting().get_settings()["path_default_social_service"]

        with open(services_info, "r") as file:
            list_services = json.load(file)

        for service in list_services:
            check_user(service=service, user=user)

    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")
