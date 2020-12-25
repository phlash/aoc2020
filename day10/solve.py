#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = [int(x) for x in f.readlines()]

# sort the values
vals.sort()

# prepend outlet value (zero)
vals.insert(0,0)

# calc device input value and append
dv = vals[len(vals)-1]+3
vals.append(dv)

# count gaps in the list (size 1-3 or invalid)
gaps=[0,0,0]
lv=vals[0]
for v in vals[1:]:
    g = v-lv
    lv = v
    if g<1 or g>3:
        print('invalid gap@',lv,v)
        sys.exit(1)
    gaps[g-1]+=1

# multiply ones and threes
print(gaps[0]*gaps[2])

# search list for permutations that are possible.
# we calculate at each entry, how many options
# exist for the next adapter (reach 1-3 away) and
# recurse into that entry, adding permutations up
# NB: we cache results (memoization) to avoid the
# repeated calculations :)
def search(idx,cac):
    # termination check
    if idx == len(vals)-1:
        return 1
    # forward search
    res = 0
    nxt = idx+1
    while nxt<len(vals) and vals[nxt]<=vals[idx]+3:
        if nxt not in cac:
            cac[nxt] = search(nxt, cac)
        res += cac[nxt]
        nxt += 1
    return res

print(search(0,{}))
