# BrainFuck compiler to python
# by umanochiocciola
#

from sys import argv

def GetSource():
    if len(argv) < 2:
        print('usage:\nmain.py <source> [cells]'); exit(1)
    
    if len(argv) > 2:
        cells = argv[2]
    else:
        cells = 30000
    
    try:
        with open(argv[1], 'r') as f:
            return f.read(), cells
    except:
        print('no such file'); exit(1)


def debug(msg, typ='info'):
    print (f'[{typ}] {msg}' )
    

debug('loading functions')

funcs = [
    "def r():\n    global ptr, cells\n    ptr += 1\n    if ptr >= len(cells):\n        ptr = 0",
    "def l():\n    global ptr, cells\n    ptr -= 1\n    if ptr < 0:\n        ptr = len(cells)-1",
    "def p():\n    global ptr, cells\n    cells[ptr] += 1\n    if cells[ptr] > 255:\n        cells[ptr] = 0",
    "def m():\n    global ptr, cells\n    cells[ptr] -= 1\n    if cells[ptr] < 0:\n        cells[ptr] = 255",
    "def d():\n    global ptr, cells\n    print(chr(cells[ptr]), end='') if cells[ptr] > 9 else print(cells[ptr], end='')",
    "def c():\n    global ptr, cells\n    newch = input('>')\n    if newch: cells[ptr] = ord(newch[0])"
]

debug('creating references')

replacer = {
    '>': 'r()',
    '<': 'l()',
    '+': 'p()',
    '-': 'm()',
    '.': 'd()',
    ',': 'c()'
}

BuildBuff = ''
progr, CELLS = GetSource()
if CELLS <= 10:
    debug('using few cells is not suggested, it saves little memory and makes your life more difficult :P', 'note')

init = f'cells = [0]*{CELLS}; ptr = 0'

signature = '# Compiled with bfpc\n'

BuildBuff += signature + '\n'.join(funcs) + '\n' + init + '\n'

debug('compiling')

INDENT = ''
i = -1
for ch in progr:
    i += 1
    if ch == '[':
        BuildBuff += INDENT+'while cells[ptr]:\n'
        INDENT += '\t'
        
    elif ch == ']':
        INDENT = '\t'*(INDENT.count('\t')-1)
    
    else:
        try:
            BuildBuff += INDENT+replacer[ch]+'\n'
        except:
            if ch != '\n' and ch != '':
                debug(f'character {i}: unknown command: {ch}', 'error')


if INDENT != '':
    debug('last loop not properly closed. Even if this works on python, it won\'t work on other compilers.', 'warn')

debug('writing file')
with open('out.py', 'w') as f:
    f.write(BuildBuff)

debug('Done!')