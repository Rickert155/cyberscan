"""
Модуль: Сканнер поддоменов
Пример исопользования:
    python3 -m cyberscan.fuzz.fuzz_domain \\ 
            --url="https://example.com" --wordlist="path/wordlist.txt"
    python3 -m cyberscan.fuzz.fuzz_domain \\
            url="https://example.com" wordlist="path/wordlist.txt"
"""
import requests
import sys
from cyberscan.core.header import Headers
from cyberscan.core.helper import CyberHelp
from cyberscan.core.colors import RED, RESET, BLUE, GREEN, BOLD, YELLOW
from cyberscan.core.core import greeting, CoreSetting, divide_line

def fuzz_subdomains(url:str):
    pass

if __name__ == "__main__":
    print(greeting())
    try:
        params = sys.argv[1:]
        if len(params) == 2 and ("url=" in params[0] or "--url=" in params[0]) and \
                ("http://" in params[0] or "https://" in params[0]) and \
                ("--wordlist=" in params[1] or "wordlist=" in params[1]):
            print(params)
    
        else:
            sys.exit(CyberHelp().help_main_menu(doc=__doc__))
    except KeyboardInterrupt:
        sys.exit(f"{RED}\nExit...{RESET}")

