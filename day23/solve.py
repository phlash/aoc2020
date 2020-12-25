#! /usr/bin/env python3
import sys, os

# load the values
#vals=[3,8,9,1,2,5,4,6,7]
vals=[3,2,7,4,6,5,1,8,9]

# add the remaining values to 1million..
for i in range(max(vals)+1,1000001):
    vals.append(i)

# performance trickery (for when we have 1 million values)
# each value is held as a tuple of (value, next, prev) ie:
# a 'linked list' through the fixed array in storage. This
# means we only have to adjust next/prev for those cups we
# are 'moving', and not copy/slice large arrays about...
# we also keep a map to value positions (constant) to avoid
# searching for destination value

cups=[]
cmap={}
mval=vals[0]
xval=vals[0]
for (i,v) in enumerate(vals):
    cups.append((v,i+1,i-1))
    cmap[v]=i
    mval = (v if v<mval else mval)
    xval = (v if v>xval else xval)

# adjust first/last to form a circular list
cups[0] = (cups[0][0],1,len(cups)-1)
cups[-1]= (cups[-1][0],0,cups[-1][2])

# play a round of the game...
def move(curr,cups):
    global mval,xval
    # pick up 3 cups after current
    pvals=[]
    pup = cups[curr][1]
    pnd = None
    nxt = pup
    for i in range(0,3):
        pvals.append(cups[nxt][0])
        pnd = nxt
        nxt = cups[nxt][1]
    cups[curr]=(cups[curr][0],nxt,cups[curr][2])
    cups[nxt]=(cups[nxt][0],cups[nxt][1],curr)
    # destination value calculation
    dval = cups[curr][0]-1
    if (dval<mval):
        dval=xval
    while dval in pvals:
        dval -= 1
        if dval<mval:
            dval=xval
    dst = cmap[dval]
    #print(pvals,cups,dval,dst,end=': ')
    # insert picked up cups one cup clockwise of dst
    nxt = cups[dst][1]
    cups[dst]=(cups[dst][0],pup,cups[dst][2])
    cups[nxt]=(cups[nxt][0],cups[nxt][1],pnd)
    cups[pup]=(cups[pup][0],cups[pup][1],dst)
    cups[pnd]=(cups[pnd][0],nxt,cups[pnd][2])
    # return next current
    return cups[curr][1]

# play 10000000 rounds, time them!
curr = 0
cnt = 0
for i in range(0,10000000):
    curr = move(curr,cups)
    cnt += 1
    if (cnt%1000)==0:
        print('\r',cnt,end='')
print()

# print the two values clockwise from 1, and their product
pos = cmap[1]
pos = cups[pos][1]
mul=cups[pos][0]
print(cups[pos][0])
pos = cups[pos][1]
mul*=cups[pos][0]
print(cups[pos][0])
print(mul)
