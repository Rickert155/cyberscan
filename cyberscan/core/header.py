"""
Модуль: Генератор заголовков HTTP

Пример использования:
    from .header import Headers

    # Можно использовать параметр create_new_agent со значением True
    # для обновления заголовков в json
    headers = Headers().create_headers(create_new_agent=False) 
"""
import json
import os
import sys
import random
from cyberscan.core.colors import RED, RESET, GREEN
from cyberscan.core.core import CoreSetting, init

class Headers:
    def __init__(self):
        self.settings = CoreSetting().get_settings()
    
    def create_json_agent(self):
        path_default_useragent_txt = self.settings["path_default_useragent_txt"] 
        path_default_useragent_json = self.settings["path_default_useragent_json"]

        agent_list = []
        if os.path.exists(path_default_useragent_txt):
            print(f"{GREEN}Читаем доступных агентов{RESET}")
            with open(path_default_useragent_txt, "r") as file:
                for line in file.readlines():
                    agent = line.strip()
                    agent_list.append(agent)
            print(f"{GREEN}Количество агентов: {len(agent_list)}{RESET}")

            with open(path_default_useragent_json, "w") as file:
                json.dump(agent_list, file, indent=4)
            print(
                    f"{GREEN}Создан список User-Agents: "
                    f"{path_default_useragent_json}{RESET}"
                    )
            return True 
        else:
            print(f"{RED}Отсутствует конфиг: {path_default_useragent_txt}{RESET}")
            return False
    
    def generate_ip(self):
        ip = ""
        for _ in range(4):
            block = random.randint(0, 255)
            ip+=f"{block}."
        
        return ip[:-1]

    def create_headers(self, create_new_agent:bool=False) -> dict[str]:
        if create_new_agent:
            self.create_json_agent()

        try:
            path_default_useragent_json = self.settings[
                    "path_default_useragent_json"
                    ]
            agent_list = []
            with open(path_default_useragent_json, "r") as file:
                data = json.load(file)
            for agent in data:
                agent_list.append(agent)
            random_agent = random.choice(agent_list)
            
            ip = self.generate_ip()
            
            headers = {
                    "User-Agent":random_agent,
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language":"ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection":"keep-alive",
                    "X-Forwarded-For":ip
                    }
            return headers
        except FileNotFoundError:
            return self.create_headers(create_new_agent=True)



if __name__ == "__main__":
    init()
    headers = Headers()
    print(headers.create_headers())
