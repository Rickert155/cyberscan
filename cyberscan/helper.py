"""
Модуль: CyberHelp. Класс для отображения подсказок по использованию
различных модулей
"""
import textwrap
from .core import greeting
from .colors import RED, RESET

class CyberHelp:
    def __init__(self):
        self.greeting = greeting().replace("-","").replace("| ","").replace("|","")

    def help_wp_plugins(self, doc:str) -> str:
        text = f"""\
        """
        text = textwrap.dedent(text)
        return text

    def help_main_menu(self, doc:str) -> str:
        text = f"""\
        {RED}{doc}{RESET}
        """
        text = textwrap.dedent(text)
        return text

    def help_wp_version(self, doc:str) -> str:
        text = f"""\
        {RED}{doc}{RESET}
        """
        text = textwrap.dedent(text)
        return text


