#! /usr/bin/env python3
import sys, re

# load the rules, held as a map (by rule id) of a list of
# alternates (can be one or more), each alternate is a
# list of sub rules, or a terminal character
vals=[]
with open('part2') as f:
    vals = f.readlines()

# parse rules
rules={}
for v in vals:
    o = v.find(':')
    r = int(v[:o])
    t = v[o+1:].strip()
    if t[0]=='"':
        # terminal char
        rules[r]=t[1]
    else:
        # list of alts
        rules[r]=[]
        for a in t.split('|'):
            # list of subs
            s = [int(x) for x in a.split()]
            rules[r].append(s)

# build an RE that matches all possible patterns in alternate
# sub lists, this is gonna get recursive!
mem={}
def build(r):
    # memoization, allows forward refs when handling recursion
    if r in mem:
        return mem[r]
    # special case rule 8, tail recursion of all patterns in
    # rule 42.. name the group so we can count them..
    if 8==r:
        mem[r] = '(?P<r8>'+build(42)+'+)'
        print('rule8',mem[r])
        return mem[r]
    # special case rule 11, nested recursion between patterns
    # in rules 42 and 31, which amounts to 1+ 42, then 1+ 31
    # however, we name these groups so we can checks balanced
    # counts later!
    if 11==r:
        b42 = '(?P<b42>'+build(42)+'+)'
        b31 = '(?P<b31>'+build(31)+'+)'
        mem[r] = '('+b42+'+'+b31+'+)'
        print('rule11',mem[r])
        return mem[r]
    v = rules[r]
    if isinstance(v,list):
        # list of alts
        t=[]
        for a in v:
            # map sequence of sub rules to a
            # sequence of expressions
            sl = [build(x) for x in a]
            # concatenate, wrap in parenthesis
            # and add to alternates list
            t.append('('+str.join('',sl)+')')
        # join alternate expressions with pipe
        # and wrap with parenthesis again..
        if len(t)>1:
            mem[r] = '('+str.join('|',t)+')'
        # ..or just plonk the only sequence in
        else:
            mem[r] = t[0]
    else:
        # terminal char, emit as-is
        mem[r] = v
    return mem[r]

mega=build(0)
#print(mega)
res=re.compile('^'+mega+'$')
rb42=re.compile(mem[42])
rb31=re.compile(mem[31])
print('compiled')

# test a value...
def test(v):
    t = v.strip()
    m = res.match(t)
    if m:
        # grab r8, b42 and b31 blocks, count matches
        r8 = -1
        b42 = -1
        b31 = -1
        if 'r8' in m.groupdict():
            r8 = len(rb42.findall(m.group('r8')))
        if 'b42' in m.groupdict():
            b42 = len(rb42.findall(m.group('b42')))
        if 'b31' in m.groupdict():
            b31 = len(rb31.findall(m.group('b31')))
        if r8+b42>b31:
            return True
    return False

# load the test values
with open('in2') as f:
    vals = f.readlines()

# test 'em!
tot = 0
for v in vals:
    tot += (1 if test(v) else 0)
print(tot)
