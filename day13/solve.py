#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# first line is our earliest departure..
dep = int(vals[0])
lst = []
# next line is a comma separated set of bus IDs..
for l in vals[1].strip().split(','):
    # retain 'x's for part2 as None
    if 'x'==l:
        lst.append(None)
    # add to ID list
    else:
        lst.append(int(l))

# Part 1: find bus ID that provides nearest departure time
nd = -1
nb = 0
for bid in lst:
    if None==bid:
        continue
    m = int((dep+bid-1)/bid)
    d = m*bid - dep
    if nd<0 or d<nd:
        nd = d
        nb = bid
print(nb,nd,nb*nd)

# Part 2: find a lowest common multiple that satifies the
# following condition for all buses:
# (multiple+list-index) % busID == 0
# We do this by finding a value for each bus in turn,
# multiplying the step size by the current busID to ensure
# the condition above remains true while searching the
# next bus
from itertools import count
mul = 0
stp = lst[0]
for l in range(1,len(lst)):
    if None==lst[l]:
        continue
    # search for a value that meets condition..
    mul = next(c for c in count(mul,stp) if (c+l)%lst[l]==0)
    # multiply the step size
    stp *= lst[l]
print(mul)
