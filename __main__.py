#!/usr/bin/env python3
# IMPORTS
import os
from sys import argv as args, stderr, stdout
import time
import yaml
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# CONSTANTS

def info(*args, **kwargs):
    print(f'{Fore.BLUE+Style.BRIGHT}info:', *args, **kwargs)

templates = {
'fetch': lambda: f'''\
version: {__verlist__}
prog:
- git fetch\
''',
'credits': lambda: f'''\
version: {__verlist__}
prog:
- echo "Made by:"
{authors()}\
'''
}

def authors():
    s = ''
    for a in authors:
        s += '- ' + a

D_REPEAT_TIME = 5.0
REPEAT_TIME = D_REPEAT_TIME
U_REPEAT_TIME = False

D_EXEC_TIME = float('inf')
EXEC_TIME = D_EXEC_TIME
U_EXEC_TIME = False

D_SCRIPT_LOC = "autoscript.yml"
SCRIPT_LOC = D_SCRIPT_LOC
U_SCRIPT_LOC = False

__version__ = '1.1.0'
__verlist__ = list(map(lambda x: int(x), __version__.split('.')))
__reldate__ = '6 November 2021'
__authors__ = ['Kerem Göksu <superkerem13@gmail.com>']

def err(explanation: str):
    print(f'{Fore.RED+Style.BRIGHT}error:{Style.RESET_ALL}', explanation, file=stderr)

def print_version():
    print(f"You are using autoscript version {__version__} released at {__reldate__}")
    exit(0)

def print_help(ec: int):
    f = stderr if ec > 0 else stdout
    print("autoscript: A simple script to automate tasks", file=f)
    print("", file=f)
    print("usage:", file=f)
    print(f"    {args[0]} [options]", file=f)
    print("", file=f)
    print("options:", file=f)
    print(f"    -i --init                 initialize a autoscript at {D_SCRIPT_LOC}")
    print(f"    -T --template <template>  initialize a autoscript according to a template at {D_SCRIPT_LOC}")
    print(f"    -t --time <time>          change execution time (type: float, default: {D_EXEC_TIME} s)", file=f)
    print(f"    -r --repeat-time <time>   change repeat time (type: float, default: {D_REPEAT_TIME} s)", file=f)
    print(f"    -s --script <script>      change the `script` to execute (type: file, default: {D_SCRIPT_LOC})", file=f)
    print("       --no-color             do not colorize output", file=f)
    print("    -h --help                 show this help message and exit", file=f)
    print("    -V --version              show version info and exit", file=f)
    exit(ec)

curarg = 1
while len(args) > curarg:
    arg = args[curarg]
    if arg in ('-i', '--init'):
        with open(D_SCRIPT_LOC, 'w') as f:
            f.write(f'version: {__verlist__}\n')
            f.write('prog:\n')
            f.write('- echo "Hello, World!"')
        exit(0)
    elif arg in ('-s', '--script'):
        if len(args) > curarg+1:
            SCRIPT_LOC = args[curarg+1]
            curarg += 1
            U_SCRIPT_LOC = True
        else:
            err('argument {arg} needs value <script>')
    elif arg in ('-T', '--template'):
        if len(args) > curarg+1:
            with open(D_SCRIPT_LOC, 'w') as f:
                t = templates.get(args[curarg+1])
                if t: f.write(t())
                else:
                    err(f'template `{args[curarg+1]}` does not exist')
                    exit(1)
                exit(0)
        else:
            err(f"argument {arg} needs value <template>")
            exit(1)
    elif arg in ('-h', '--help'): print_help(0)
    elif arg in ('-V', '--version'): print_version()
    elif arg == '--no-color':
        Fore.BLUE = ''
        Fore.RED = ''
        Style.BRIGHT = ''
    elif arg in ('-t', '--time'):
        if len(args) > curarg+1:
            EXEC_TIME = float(args[curarg+1])
            curarg += 1
            U_EXEC_TIME = True
        else:
            err(f"argument {arg} needs value <time>")
            print_help(1)
    elif arg in ('-r', '--repeat-time'):
        if len(args) > curarg+1:
            REPEAT_TIME = float(args[curarg+1])
            curarg += 1
            U_REPEAT_TIME = True
        else:
            err(f"argument {arg} needs value <time>")
            print_help(1)
    else:
        err(f"unknown argument: {arg}")
        print_help(1)
    curarg += 1

t = time.time()

try:
    with open(SCRIPT_LOC) as f:
        src = yaml.safe_load(f.read())
        progs = src.get('prog')
        if not progs and progs != []:
            err('`prog` for script not provided')
            exit(1)
        exec_time = src.get('time')
        if exec_time: EXEC_TIME = EXEC_TIME if U_EXEC_TIME else float(exec_time)
        repeat_time = src.get('repeat')
        if repeat_time: REPEAT_TIME = REPEAT_TIME if U_REPEAT_TIME else float(repeat_time)

except FileNotFoundError as e:
    err(f'script at `{SCRIPT_LOC}` not found? maybe you need to create it. run `{args[0]} --init` to initialize a script')
    exit(0)

info('starting...')
try:
    while time.time()-t < EXEC_TIME:
        for prog in progs:
            ec = os.system(prog)
            if ec != 0:
                err(f'`{prog}` encountered an error')
                exit(ec)
        time.sleep(REPEAT_TIME)
except KeyboardInterrupt: pass
info('closing...')
