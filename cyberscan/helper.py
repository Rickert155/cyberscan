"""
Модуль: CyberHelp. Класс для отображения подсказок по использованию
различных модулей
"""
import textwrap
from .core import greeting

class CyberHelp:
    def __init__(self):
        self.greeting = greeting().replace("-","").replace("| ","").replace("|","")

    def help_wp_plugins(self, doc:str) -> str:
        text = f"""\
        {self.greeting}\n{doc} 
        """
        text = textwrap.dedent(text)
        return text



