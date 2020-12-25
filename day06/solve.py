#! /usr/bin/env python3

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# count the repeated letters in each blank-line-separated group
# sum all those answers where repeat count = number of lines.
tot1=0
tot2=0
lns=0
cnt={}
def count(n, l):
    t1=0
    t2=0
    for c in n:
        if n[c]==l:
            t2+=1
        t1+=1
    return (t1,t2)

for line in vals:
    line=line.strip()
    if len(line)==0:
        # count done, add to sum and reset
        x = count(cnt, lns)
        tot1 += x[0]
        tot2 += x[1]
        cnt = {}
        lns = 0
        continue
    for c in line:
        if c in cnt:
            cnt[c]=cnt[c]+1
        else:
            cnt[c]=1
    lns = lns+1
x = count(cnt, lns)
tot1 += x[0]
tot2 += x[1]
print(tot1, tot2)
