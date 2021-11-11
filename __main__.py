#!/usr/bin/env python3
# IMPORTS
from os import system, path
realpath = path.realpath

import time
import colorama
from util import *
colorama.init(autoreset=True)

# ARGUMENT PARSER

import args
psd = args.parse_args()
debug = psd.debug
exec_time = psd.exec_time
repeat_time = psd.repeat_time
script_loc = psd.script_loc

# LOAD SCRIPT

if debug: info('loading script...')

import importer

progs = importer.Importer(realpath(script_loc), [realpath(script_loc)]).import_(exec_time, repeat_time).prog

if debug: info('loaded script!')

# START SCRIPT

t = time.time()

info('starting...')
try:
    while time.time()-t < exec_time:
        for prog in progs:
            if debug: info(f'executing `{prog}`...')
            ec = system(prog)
            if ec != 0:
                err(f'`{prog}` encountered an error')
                exit(ec)
            if debug: info(f'executed `{prog}`!')
        time.sleep(repeat_time)
except KeyboardInterrupt: pass
info('closing...')
