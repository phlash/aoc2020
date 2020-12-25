#! /usr/bin/env python3

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# calculate boarding pass row/seat and ID
# find highest ID
high=0
idmap={}
for line in vals:
    # 'binary space partitioning' aka binary numbers
    # mapped as 7-bit (F=0,B=1), then 3-bit (R=1,L=0)
    # so we assemble the bits..
    row=0
    for i in range(0,7):
        row <<= 1
        row |= (1 if line[i]=='B' else 0)
    col=0
    for i in range(7,10):
        col <<= 1
        col |= (1 if line[i]=='R' else 0)
    sid = row*8+col
    if sid>high:
        high = sid
    idmap[sid]=1
print(high)
# now find a gap in the seat ids with a seat either side
for i in range(1,high):
    if i not in idmap:
        if (i-1) in idmap and (i+1) in idmap:
            print(i)
            break
