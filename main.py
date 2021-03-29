from sys import argv

if len(argv) < 2:
    print("missing file argument"); exit(1)

try:
    with open(argv[1], 'r') as f:
        program = f.read()
except:
    print("no such file"); exit(1)

def debug(txt, typ='info'):
    print(f'[{typ}] {txt}')

try:
    cells = int(argv[2])
except:
    cells = 16
    debug('using deafult tape len (16) because not specified', 'note')

debug('-- BBWB Compiler started --')
debug('setting up')

funcs = {
    'def p():\n\tglobal buff\n\tbuff += 1\n\tif buff > 255: buff = 0':              '+',
    'def m():\n\tglobal buff\n\tbuff -= 1\n\tif buff < 0: buff = 255':              '-',
    'def w():\n\tglobal buff, ptr, tape\n\ttape[ptr] = buff':                       '^',
    'def r():\n\tglobal buff, ptr, tape\n\tbuff = tape[ptr]':                       'v',
    f'def d():\n\tglobal buff, ptr, tape\n\tptr = ptr-1 if ptr > 0 else {cells-1}':   '<',
    f'def i():\n\tglobal buff, ptr, tape\n\tptr = ptr+1 if ptr+1 < {cells} else 0': '>',
    'def dt():\n\tglobal buff, ptr, tape\n\tprint(buff, end="", flush=True)':       '.',
    'def cl():\n\tglobal buff, ptr, tape\n\tprint(chr(buff), end="", flush=True)':  ':',
    'def cm():\n\tglobal buff, ptr, tape\n\tbuff = int(input("i> "))':              ',',
    'def sc():\n\tglobal buff, ptr, tape\n\tbuff = ord(input("c> "))':           ';'
}

debug('initializing')

signature = '# transpiled to python with BBWBC\n# https://github.com/umanochiocciola/bbwb\n'
init = f'\ntape = [0]*{cells}\nptr = 0\nbuff = 0\n'

OUTPUT = signature
for i  in funcs:               # if a program doesn't use a command, why would you include it?
    if funcs[i] in program:
        OUTPUT += i + '\n'

OUTPUT += init
    

debug('creating references')

repls = {
    '+': 'p()',
    '-': 'm()',
    '#': 'buff = 0',
    '^': 'w()',
    'v': 'r()',
    '<': 'd()',
    '>': 'i()',
    '.': 'dt()',
    ':': 'cl()',
    ',': 'cm()',
    ';': 'sc()',
    '[': '\nwhile tape[ptr]:',
    '@': 'print(tape, ptr, buff)'
}

debug('compiling')

loops = 0
for ch in program:
    
    if ch == ']': OUTPUT = OUTPUT[:-1] + '\n'# we need to remove last ";"
    if not (ch in repls): continue
    
    OUTPUT += repls[ch]+';'
    if ch == '[': OUTPUT = OUTPUT[:-1]       # obviously we can't have "while:;"

OUTPUT += '0'

debug('writing to out.py')

with open('out.py', 'w') as f:
    f.write(OUTPUT)

debug('done!')
