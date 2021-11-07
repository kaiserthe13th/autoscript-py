#!/usr/bin/env python3
# IMPORTS
from os import system, path
realpath = path.realpath
from sys import argv as args, stderr, stdout
import time
import yaml
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

# CONSTANTS

## D_{x} = Default for {x}

DEBUG = False

D_REPEAT_TIME = 5.0
REPEAT_TIME = D_REPEAT_TIME

D_EXEC_TIME = float('inf')
EXEC_TIME = D_EXEC_TIME

## Script Location
D_SCRIPT_LOC = "autoscript.yml"
SCRIPT_LOC = D_SCRIPT_LOC

__version__ = '2.0.0'
__verlist__ = list(map(lambda x: int(x), __version__.split('.'))) # This turns version into a list of numbers (x, y, z being a number, x.y.z -> [x, y, z])
__reldate__ = '7 November 2021' # Release Date
__authors__ = ['Kerem Göksu <superkerem13@gmail.com>'] # Authors

## Templates
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

# UTILS

info = lambda *args, **kwargs: print(f'{Fore.BLUE+Style.BRIGHT}info:', *args, **kwargs)
err = lambda explanation: print(f'{Fore.RED+Style.BRIGHT}error:{Style.RESET_ALL}', explanation, file=stderr)

def authors():
    s = ''
    for a in authors:
        s += '- ' + a

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

# ARGUMENT PARSER

info('parsing arguments...')

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
        else:
            err('argument {arg} needs value <script>')
            print_help(1)
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
            print_help(1)
    elif arg in ('-h', '--help'): print_help(0)
    elif arg in ('-V', '--version'): print_version()
    elif arg in ('-d', '--debug'):
        DEBUG = True
    elif arg == '--no-color':
        # set every used Fore, Back, Style to ''
        Fore.BLUE = ''
        Fore.RED = ''
        Style.BRIGHT = ''
    elif arg in ('-t', '--time'):
        if len(args) > curarg+1:
            EXEC_TIME = float(args[curarg+1])
            curarg += 1
        else:
            err(f"argument {arg} needs value <time>")
            print_help(1)
    elif arg in ('-r', '--repeat-time'):
        if len(args) > curarg+1:
            REPEAT_TIME = float(args[curarg+1])
            curarg += 1
        else:
            err(f"argument {arg} needs value <time>")
            print_help(1)
    else:
        err(f"unknown argument: {arg}")
        print_help(1)
    curarg += 1

info('parsed arguments!')

# LOAD SCRIPT

if DEBUG: info('loading script...')

class Import:
    def __init__(self, visited, prog):
        self.visited, self.prog = (
            visited, prog
        )

class Importer:
    def __init__(self, loc: str, visited: list):
        self.loc = loc
        self.visited = visited
    
    def import_(self):
        global EXEC_TIME
        global REPEAT_TIME
        try:
            with open(self.loc) as f:
                src = yaml.safe_load(f.read())
                progs_ = src.get('prog')
                if not progs_ and progs_ != []:
                    err('`prog` for script not provided')
                    exit(1)
                EXEC_TIME = src.get('time') or EXEC_TIME
                REPEAT_TIME = src.get('repeat') or REPEAT_TIME
                imports = src.get('import')
                if imports:
                    if isinstance(imports, str):
                        if realpath(imports) not in self.visited:
                            imported = Importer(realpath(imports), self.visited + [realpath(i)]).import_()
                            progs_ += imported.prog
                            self.visited += imported.visited
                    elif isinstance(imports, list):
                        for i in imports:
                            if realpath(i) not in self.visited:
                                imported = Importer(realpath(i), self.visited + [realpath(i)]).import_()
                                progs_ += imported.prog
        except FileNotFoundError as e:
            err(f'script at `{self.loc}` not found? maybe you need to create it. run `{args[0]} --init` to initialize a script')
            exit(1)
        return Import(self.visited, progs_)

progs = Importer(realpath(SCRIPT_LOC), [realpath(SCRIPT_LOC)]).import_().prog

if DEBUG: info('loaded script!')

# START SCRIPT

t = time.time()

info('starting...')
try:
    while time.time()-t < EXEC_TIME:
        for prog in progs:
            if DEBUG: info(f'executing `{prog}`...')
            ec = system(prog)
            if ec != 0:
                err(f'`{prog}` encountered an error')
                exit(ec)
            if DEBUG: info(f'executed `{prog}`!')
        time.sleep(REPEAT_TIME)
except KeyboardInterrupt: pass
info('closing...')
