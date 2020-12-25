#! /usr/bin/env python3
from functools import reduce

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# walk the array, wrap at the end of a line, count hashes
# we walk multiple spans (see below) aggregating multiple
# hash counts, then multiply them all together
spans=[1,3,5,7,-1]  # -1 indicates 'every other line'
pos=[0,0,0,0,0]
hashes=[0,0,0,0,0]
l=0
for line in vals:
    # nuke that whitespace!
    line = line.rstrip()
    # calculate for each span..
    for i in range(0,len(pos)):
        x = pos[i]
        s = spans[i]
        # skip odd lines if span<0
        if s<0 and (l%2)!=0:
            continue
        # ensure positive span
        if s<0:
            s = -s
        # hit test at current position
        if line[x] == '#':
            hashes[i] += 1
        # walk right by span (wrapped)
        x = (x+s)%len(line)
        pos[i] = x
    l += 1
tot = reduce(lambda x,y : x*y, hashes)
print(hashes, l, tot)
