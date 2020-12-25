#! /usr/bin/env python3
import sys

# load the values
vals=[]
with open('input') as f:
    vals = f.readlines()

# parse ingredients and allegens..
lins=[]
ings={}
algs={}
for v in vals:
    v = v.strip()
    o = v.find('(contains')
    ing = [x.strip() for x in v[:o].split()]
    alg = [x.strip() for x in v[o+9:-1].split(',')]
    lins.append([ing,alg])
    for i in ing:
        ings[i]=True
    for a in alg:
        algs[a]=True

# try all permutations of ingredient and allergen,
# check this against input data: if we find the
# allergen but not the ingredient, it cannot be
# that allergen. If we eliminate all allergens then
# we have an ingredient that cannot be an allergen.
impos=[]
danger=[]
for i in ings:
    cnt = 0
    for a in algs:
        for l in lins:
            if (i not in l[0]) and (a in l[1]):
                cnt += 1
                break
    if cnt==len(algs):
        impos.append(i)
    else:
        danger.append(i)
print(len(impos),len(danger),danger)

# now count occurrances of impossible allergens
cnt = 0
for l in lins:
    for i in impos:
        if i in l[0]:
            cnt += 1
print('part1',cnt)

# part2 - now eliminate unknowns using same algorithm as
# above, find lines where allergen exists but they don't
for d in danger:
    can=[]
    for a in algs:
        cant = False
        for l in lins:
            if (d not in l[0]) and (a in l[1]):
                cant = True
                break
        if not cant:
            can.append(a)
    print(d,can)
