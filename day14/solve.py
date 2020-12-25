#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# Yay - more emulation, this time a memory fill DSL..
mem={}
sms=0
cms=0
m2={}
fms=0
def execute(ins):
    global mem, sms, cms, m2, fms
    if ins.startswith('mask'):
        o = ins.find('=')
        if o<0:
            print('invalid:',ins)
            sys.exit(1)
        ms = ins[o+1:].strip()
        sms= int(ms.replace('X','0'),2)
        cms= int(ms.replace('X','1'),2)
        fms= int(ms.replace('1','0').replace('X','1'),2)
    elif ins.startswith('mem'):
        o = ins.find('[')
        p = ins.find(']',o) if o>0 else o
        q = ins.find('=',p) if p>0 else p
        if q<0:
            print('invalid:',ins)
            sys.exit(2)
        add = int(ins[o+1:p])
        val = int(ins[q+1:].strip())
        # part1, simple masked set
        mem[add] = (val | sms) & cms
        # part2, forced '1's and 'floating' address bits
        add = add | sms
        ads = [add]
        for b in range(0,36):
            tms = 1<<b
            if tms & fms:
                fcl = [x & ~tms for x in ads]   # clear floating bit
                fst = [x | tms for x in ads]    # set floating bit
                ads = fcl + fst
        for a in ads:
            m2[a] = val
    else:
        print('invalid:',ins)
        sys.exit(3)

for l in vals:
    execute(l)

tot = 0
for a in mem:
    tot += mem[a]
print('part1',tot)
tot = 0
for a in m2:
    tot += m2[a]
print('part2',tot)
