#! /usr/bin/env python3
import sys
# a little different this time - input is here
srt = [19,0,5,1,10,13]

# now iterate 2020 cycles of the daft rules to
# produce a number from these, and record against
# each number, the list of turns it appears on..
lst={}
prv=0
for t in range(0,30000000):
    if t<len(srt):
        # just emit the starting value
        prv = srt[t]
        lst[prv]=[t]
    else:
        # follow the rules based on last number
        # 1. only seen once before..
        if len(lst[prv])<2:
            # emit 0
            prv = 0
        # 2. otherwise..
        else:
            # emit different between last two appearances
            prv = lst[prv][-1]-lst[prv][-2]
        if prv in lst:
            lst[prv].append(t)
        else:
            lst[prv]=[t]
    if (2019==t):
        print('\npart1:',t,prv)
    if (t%100000)==0:
        print('\r',t,end='')
print('\npart2:',t,prv)
