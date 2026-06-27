import sys
from cyberscan.cli import COMMANDS
from cyberscan.core.core import divide_line
from cyberscan.cms.wp_plugins import scanWordPressPlugins
from cyberscan.cms.wp_version import scanWordPressVersion
from cyberscan.social.cyberwarnuser import cyberwarnuser
from cyberscan.fuzz.fuzz_subdomain import fuzz_subdomains
from cyberscan.fuzz.fuzz_dirs import fuzz_dirs
from cyberscan.fuzz.get_links import get_links
from cyberscan.fuzz.get_comments import get_comments

def tests():
    user_url = None
    params = sys.argv[1:]
    if len(params) > 0:
        if params[0].startswith("https://") or params[0].startswith("http://"):
            user_url = params[0]
        
    counte_module = 0
    for command in COMMANDS:
        counte_module+=1

        module = COMMANDS[command]["module"]
        args = COMMANDS[command]["args"]
        template = COMMANDS[command]["template"]
        mode_test = True
        
        if user_url:
            url = user_url
        else:
            url = COMMANDS[command]["example_url"]
        
        example_wordlist = COMMANDS[command].get("example_wordlist")
        
        data = {}
        data["template"] = template
        data["mode_test"] = mode_test
        data["--url"] = url
        data["--workers"] = 20
        
        if example_wordlist:
            data["--wordlist"] = example_wordlist
        
        print(
                f"{divide_line()}\n"
                f"| Module [{counte_module}]: {command}"
                )
        
        module(args=data)
        

if __name__ == "__main__":
    try:
        tests()
    except KeyboardInterrupt:
        sys.exit("\nExit...")
