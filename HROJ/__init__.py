from HROJ.user import *
from HROJ.problem import *
from HROJ.submission import *

from time import strftime

class color:
    header = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    orange = '\033[38;5;214m'

    whitebg = '\033[7m'
    redbg = '\033[41m'
    greenbg = '\033[102m'
    yellowbg = '\033[43m'
    bluebg = '\033[44m'
    graybg = "\033[48:5m"
    blackbg = '\u001b[40m'

    gray = '\033[37m'
    reset = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    
    include = '\033[95m'
    
def logthis(text,mode):
    colors = {
        "danger" : color.red,
        "warning" : color.yellow,
        "success" : color.green,
        "info" : color.blue
    }
    print(f"[{colors[mode]}{strftime('%X')}{color.reset}] {text}")