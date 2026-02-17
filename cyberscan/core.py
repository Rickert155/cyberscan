import textwrap
import os
import json
from .colors import RED, RESET, BOLD, GREEN
from . import (
        __author__, 
        __version__, 
        __project__, 
        __authorurl__,
        __license__
        )

class CoreSetting:
    
    def __init__(self):
        self.settings_path = "data/settings.json"

    def get_settings(self, show_settings:bool=False):
        """
        Получаем данные из настроек/создаем дефолтный json
        show_settings - отобразить настройки - True, по умолчанию 
        не выводятся
        """
        if not os.path.exists(self.settings_path):
            data = {
                    "path_default_useragent_txt":"data/useragent.txt",
                    "path_default_useragent_json":"data/agent.json",
                    "path_default_wp_plugin":"data/wp_plagins.txt"
                    }
            with open(self.settings_path, "w") as file:
                json.dump(data, file, indent=4)
        with open(self.settings_path, "r") as file:
            data = json.load(file)

        if show_settings:
            print(f"\nsettings:")
            for key, value in data.items():
                print(f"{key}:\t{value}")

        return data

    def update_settings(self, user_key:str, user_value:str):
        """Обновление настроек по ключу и значению"""
        try:
            with open(self.settings_path, "r") as file:
                data = json.load(file)

            data[user_key] = user_value
            with open(self.settings_path, "w") as file:
                json.dump(data, file, indent=4)
            return "ok"
        except Exception as error:
            return error
    
    def check_path_config(self) -> list[ list[str] | None ]:
        """Проверка наличия пользовательских файлов конфигураций"""
        with open(self.settings_path, "r") as file:
            data = json.load(file)

        found_config = []
        not_found_config = []
        for key, value in data.items():
            if "path" in key:
                if os.path.exists(value):
                    found_config.append(value)
                    print(f"{GREEN}[OK] config: {value}{RESET}")
                else:
                    not_found_config.append(value)
                    print(f"{RED}[WARNING] config not found: {value}{RESET}")

        return found_config, not_found_config


def greeting():
    greet_text = f"""\
    {BOLD}author:       {__author__}{RESET}\t{GREEN}{__authorurl__}{RESET}
    {BOLD}project:      {__project__}{RESET}\t{GREEN}{__license__}{RESET}      
    {BOLD}version:      {__version__}{RESET}
    """
    greet_text = textwrap.dedent(greet_text)
    return greet_text

def init():
    print(greeting())
    settings = CoreSetting()
    settings.get_settings(show_settings=False)
    settings.check_path_config()


