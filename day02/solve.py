#! /usr/bin/env python3

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# search for valid entries
pt1=0
pt2=0
for a in vals:
    # parse the line
    p = a.split(' ', 3)
    (mn, mx) = [int(x) for x in p[0].split('-')]
    lt = p[1][0]
    # part#1: count occurrances of lt in string
    n = 0
    for l in p[2]:
        if l==lt:
            n = n+1
    # does it fall within min-max range (inclusive)
    if n>=mn and n<=mx:
        pt1 = pt1+1

    # part#2: check if lt occurs at positions mn, mx (base1)
    n = 0
    if len(p[2])>mn and p[2][mn-1]==lt:
        n = n+1
    if len(p[2])>mx and p[2][mx-1]==lt:
        n = n+1
    # exactly one occurance?
    if n==1:
        pt2 = pt2+1
print('counts', pt1, pt2)
