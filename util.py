# UTILS for autoscript
from __init__ import __version__, __verlist__, __authors__, __reldate__, D_SCRIPT_LOC, D_EXEC_TIME, D_REPEAT_TIME
from colorama import Fore, Style
from sys import stderr, stdout, argv

info = lambda *args, **kwargs: print(f'{Fore.BLUE+Style.BRIGHT}info:', *args, **kwargs)
err = lambda explanation: print(f'{Fore.RED+Style.BRIGHT}error:{Style.RESET_ALL}', explanation, file=stderr)

def authors():
    s = ''
    for a in __authors__:
        s += '- ' + a

def print_version():
    print(f"You are using autoscript version {__version__} released at {__reldate__}")
    exit(0)

def print_help(ec: int):
    f = stderr if ec > 0 else stdout
    print("autoscript: A simple script to automate tasks", file=f)
    print("", file=f)
    print("usage:", file=f)
    print(f"    {argv[0]} [options]", file=f)
    print("", file=f)
    print("options:", file=f)
    print(f"    -i --init                 initialize a autoscript at {D_SCRIPT_LOC}", file=f)
    print(f"    -T --template <template>  initialize a autoscript according to a template at {D_SCRIPT_LOC}", file=f)
    print(f"    -t --time <time>          change execution time (type: float, default: {D_EXEC_TIME} s)", file=f)
    print(f"    -r --repeat-time <time>   change repeat time (type: float, default: {D_REPEAT_TIME} s)", file=f)
    print(f"    -s --script <script>      change the `script` to execute (type: file, default: {D_SCRIPT_LOC})", file=f)
    print("    -d --debug                show debug info", file=f)
    print("       --no-color             do not colorize output", file=f)
    print("    -h --help                 show this help message and exit", file=f)
    print("    -V --version              show version info and exit", file=f)
    exit(ec)

## Templates
TEMPLATES = {
    # Fetch Template
    'fetch': lambda: f'''\
    version: {__verlist__}
    prog:
    - git fetch\
    ''',

    # Credits Template
    'credits': lambda: f'''\
    version: {__verlist__}
    prog:
    - echo "Made by:"
    {authors()}\
    '''
}
