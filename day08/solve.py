#! /usr/bin/env python3
# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

def emulate(prog):
    # emulation of a very simple CPU =)
    cnt=0
    pc=0
    acc=0
    vis=[]
    line=''
    lpc=0
    mpc=0
    # we emulate until we revisit an address (infinite loop)
    # or run off either end
    while (pc not in vis) and pc>=0 and pc<len(prog):
        # parse instruction <op> <val>
        line = prog[pc].strip()
        vis.append(pc)
        lpc = pc
        if pc>mpc:
            mpc = pc
        o = line.find(' ')
        if o<0:
            print('no separator:',line)
            break
        op = line[:o].strip()
        n = 0
        try:
            n = int(line[o:].strip())
        except:
            print('invalid val:',line)
            break
        if op == 'nop':
            pc += 1
        elif op == 'acc':
            acc += n
            pc += 1
        elif op == 'jmp':
            pc += n
        else:
            print('invalid op:',line)
            break
        cnt += 1
    return (acc, cnt, mpc, lpc, pc)

# now we brute force excute all variations of the program
# with jmp->nop, then nop->jmp until it terminates with
# pc == len(prog)
emu=0
edit=0
fnd='jmp'
sub='nop'
while edit<len(vals):
    prog = list(vals)   # clone as we are editing
    while edit<len(prog) and not prog[edit].startswith(fnd):
        edit += 1
    if edit<len(prog):
        # found the next instruction, change it
        prog[edit] = prog[edit].replace(fnd, sub)
        (acc, cnt, mpc, lpc, pc) = emulate(prog)
        emu += 1
        print('\r',emu,fnd,'->',sub,'@',edit,end='')
        if pc==len(prog):
            print('\n',fnd,'->',sub,'@',edit,'=',acc)
            break
        edit += 1
    else:
        # off the end, switch to nop->jmp or bail
        if fnd=='jmp':
            fnd='nop'
            sub='jmp'
            edit=0
        else:
            print('oops, nothing worked')
            break
