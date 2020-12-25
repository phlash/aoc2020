#! /usr/bin/env python3
# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# parse the following syntax into a map of:
# colour->contains->[list of colours]
# <colour> bags contain [<n> <colour> bag[s][, ...]|no other bags]
cmap = {}
for line in vals:
    o = line.find('bags contain')
    if o<0:
        print('no "bags contain"?', line)
        continue
    col = line[:o].strip()
    # check for terminal colour
    if line.find('no other bags', o+12)>0:
        if col in cmap:
            print('already mapped?', col)
        else:
            cmap[col]=[]
        continue
    # non-terminal, split and parse each mapped colour
    for part in line[o+12:].split(','):
        part = part.strip()
        o = part.find('bag')
        if o<0:
            print('no "bag"?', part)
            continue
        s = part.find(' ')
        n = s if s<0 else int(part[:s])
        if n<0:
            print('no "<n>"?', part)
            continue
        mc = part[s:o].strip()
        if col in cmap:
            cmap[col].append((n,mc))
        else:
            cmap[col]=[(n,mc)]

# recursively walk 'down' the map, if we find a specifc
# colour anywhere, return True to record the top colour
def search(dep,srt,src):
    # found search colour?
    res=False
    if srt==src:
        res=True
        #print(dep)
    else:
        for (n,col) in cmap[srt]:
            if search(dep+'/'+col,col,src):
                res=True
                break
    return res

cnt=0
for col in cmap:
    # don't include search term itself (must be in another bag)
    if col=='shiny gold':
        continue
    if search(col,col,'shiny gold'):
        cnt+=1
print(cnt)

# starting at shiny gold bag, count all included bags
def count(srt):
    res=0
    for (n,col) in cmap[srt]:
        res += (n+n*count(col))
    return res

print(count('shiny gold'))
