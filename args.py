from util import *
from sys import argv as args

class Args:
    def __init__(self, debug, repeat_time, exec_time, script_loc) -> None:
        self.debug = debug
        self.repeat_time = repeat_time
        self.exec_time = exec_time
        self.script_loc = script_loc

def parse_args() -> Args:
    info('parsing arguments...')
    
    # mutants
    debug = False
    repeat_time = D_REPEAT_TIME
    exec_time = D_EXEC_TIME
    script_loc = D_SCRIPT_LOC
    
    # parse
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
                script_loc = args[curarg+1]
                curarg += 1
            else:
                err('argument {arg} needs value <script>')
                print_help(1)
        elif arg in ('-T', '--template'):
            if len(args) > curarg+1:
                with open(D_SCRIPT_LOC, 'w') as f:
                    t = TEMPLATES.get(args[curarg+1])
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
            debug = True
        elif arg == '--no-color':
            # set every used Fore, Back, Style to ''
            Fore.BLUE = ''
            Fore.RED = ''
            Style.BRIGHT = ''
        elif arg in ('-t', '--time'):
            if len(args) > curarg+1:
                exec_time = float(args[curarg+1])
                curarg += 1
            else:
                err(f"argument {arg} needs value <time>")
                print_help(1)
        elif arg in ('-r', '--repeat-time'):
            if len(args) > curarg+1:
                repeat_time = float(args[curarg+1])
                curarg += 1
            else:
                err(f"argument {arg} needs value <time>")
                print_help(1)
        else:
            err(f"unknown argument: {arg}")
            print_help(1)
        curarg += 1
    info('parsed arguments!')

    return Args(debug, repeat_time, exec_time, script_loc)
