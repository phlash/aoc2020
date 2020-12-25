#! /usr/bin/env python3
import sys, re

# load the fields, your ticket and others
flds=[]
with open('fields') as f:
    flds = f.readlines()
you=[]
with open('yours') as f:
    you = [int(x) for x in f.readline().split(',')]
oth=[]
with open('others') as f:
    for l in f.readlines():
        oth.append([int(x) for x in l.split(',')])

# parse the fields into a map of named lists of ranges
rng = {}
src = re.compile('([^:]+): (\d+)-(\d+) or (\d+)-(\d+)')
for fld in flds:
    m = src.match(fld)
    if m:
        nam = m.group(1)
        r1  = range(int(m.group(2)),int(m.group(3))+1)
        r2  = range(int(m.group(4)),int(m.group(5))+1)
        if nam in rng:
            rng[nam].append(r1,r2)
        else:
            rng[nam] = [r1,r2]
    else:
        print('unparseable:',fld)
        sys.exit(1)

def getinvalid(tkt):
    global rng
    rv = []
    # find all invalid values in supplied ticket
    for v in tkt:
        f = False
        for l in rng.values():
            for r in l:
                if v in r:
                    f = True
        if not f:
            rv.append(v)
    return rv

# part1: find all invalid values in other tickets, keep valid tickets
inv=[]
val=[]
for t in oth:
    i = getinvalid(t)
    if len(i)==0:
        # valid, keep it
        val.append(t)
    else:
        inv.extend(i)
print('part1',len(inv), sum(inv))

# part2: check your ticket is valid =)
if len(getinvalid(you))>0:
    print('invalid your ticket!')
    sys.exit(1)

# deduce columns by checking column values against ranges until they fit
# NB: we don't need to find everything, as long as we have 'departure X'
# NBB: find *all* possible column names, we might need to fudge later..
cols={}
for col in range(0,len(you)):
    x=[]
    for t in val:
        x.append(t[col])
    #print('srch',col,x)
    d = []
    for n in rng:
        d = []
        ok = True
        for v in x:
            f = False
            for r in rng[n]:
                if v in r:
                    f = True
            if not f:
                ok = False
                d.append(v)
                break
        #print('  ',n,ok,d)
        if ok:
            if col in cols:
                cols[col].append(n)
            else:
                cols[col]=[n]
            #break
    if len(d)>0:
        print('fail',col,d)

# multiple all 'departure X' columns in your ticket
mul=1
for col in cols:
    print(col, cols[col])
